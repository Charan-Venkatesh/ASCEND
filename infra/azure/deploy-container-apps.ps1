param(
  [string]$ResourceGroup = "rg-ascend-os-prod",
  [string]$Location = "eastus",
  [string]$EnvironmentName = "cae-ascend-os",
  [string]$RegistryName = "acrascendosprod",
  [string]$BackendImage = "ascend-backend:latest",
  [string]$FrontendImage = "ascend-frontend:latest",
  [string]$PostgresAdmin = "ascendadmin",
  [string]$PostgresPassword,
  [string]$SecretKey,
  [string]$NvidiaApiKey = "",
  [string]$OpenAiApiKey = ""
)

if (-not $PostgresPassword) { throw "PostgresPassword is required." }
if (-not $SecretKey) { throw "SecretKey is required." }

$ErrorActionPreference = "Stop"
$PostgresServer = "psql-ascend-os-prod"
$DatabaseName = "ascend_os"
$KeyVaultName = "kv-ascend-os-prod"
$RedisName = "redis-ascend-os-prod"

az group create --name $ResourceGroup --location $Location
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

az acr create --resource-group $ResourceGroup --name $RegistryName --sku Basic --admin-enabled true
az acr build --registry $RegistryName --image $BackendImage ./backend
az acr build --registry $RegistryName --image $FrontendImage ./frontend

az postgres flexible-server create --resource-group $ResourceGroup --name $PostgresServer --location $Location --admin-user $PostgresAdmin --admin-password $PostgresPassword --sku-name Standard_B1ms --tier Burstable --storage-size 32 --version 16 --yes
az postgres flexible-server db create --resource-group $ResourceGroup --server-name $PostgresServer --database-name $DatabaseName
az postgres flexible-server firewall-rule create --resource-group $ResourceGroup --name $PostgresServer --rule-name allow-azure --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0

az redis create --resource-group $ResourceGroup --name $RedisName --location $Location --sku Basic --vm-size c0
$RedisKey = az redis list-keys --resource-group $ResourceGroup --name $RedisName --query primaryKey -o tsv

az keyvault create --resource-group $ResourceGroup --name $KeyVaultName --location $Location
$DatabaseUrl = "postgresql+psycopg://${PostgresAdmin}:${PostgresPassword}@${PostgresServer}.postgres.database.azure.com:5432/${DatabaseName}?sslmode=require"
$RedisUrl = "redis://:${RedisKey}@${RedisName}.redis.cache.windows.net:6380/0?ssl_cert_reqs=required"
az keyvault secret set --vault-name $KeyVaultName --name "database-url" --value $DatabaseUrl
az keyvault secret set --vault-name $KeyVaultName --name "redis-url" --value $RedisUrl
az keyvault secret set --vault-name $KeyVaultName --name "secret-key" --value $SecretKey
az keyvault secret set --vault-name $KeyVaultName --name "nvidia-api-key" --value $NvidiaApiKey
az keyvault secret set --vault-name $KeyVaultName --name "openai-api-key" --value $OpenAiApiKey

az containerapp env create --resource-group $ResourceGroup --name $EnvironmentName --location $Location
$LoginServer = az acr show --name $RegistryName --query loginServer -o tsv
$AcrUser = az acr credential show --name $RegistryName --query username -o tsv
$AcrPass = az acr credential show --name $RegistryName --query "passwords[0].value" -o tsv

az containerapp create --resource-group $ResourceGroup --environment $EnvironmentName --name ascend-backend --image "$LoginServer/$BackendImage" --registry-server $LoginServer --registry-username $AcrUser --registry-password $AcrPass --target-port 8000 --ingress external --min-replicas 1 --max-replicas 3 --secrets "database-url=$DatabaseUrl" "redis-url=$RedisUrl" "secret-key=$SecretKey" "nvidia-api-key=$NvidiaApiKey" "openai-api-key=$OpenAiApiKey" --env-vars "DATABASE_URL=secretref:database-url" "REDIS_URL=secretref:redis-url" "SECRET_KEY=secretref:secret-key" "NVIDIA_API_KEY=secretref:nvidia-api-key" "OPENAI_API_KEY=secretref:openai-api-key" "QDRANT_URL=http://qdrant:6333" "FRONTEND_ORIGIN=https://initial.local"
$BackendUrl = az containerapp show --resource-group $ResourceGroup --name ascend-backend --query properties.configuration.ingress.fqdn -o tsv

az containerapp create --resource-group $ResourceGroup --environment $EnvironmentName --name ascend-frontend --image "$LoginServer/$FrontendImage" --registry-server $LoginServer --registry-username $AcrUser --registry-password $AcrPass --target-port 3000 --ingress external --min-replicas 1 --max-replicas 3 --env-vars "NEXT_PUBLIC_API_BASE_URL=https://$BackendUrl/api/v1"
$FrontendUrl = az containerapp show --resource-group $ResourceGroup --name ascend-frontend --query properties.configuration.ingress.fqdn -o tsv
az containerapp update --resource-group $ResourceGroup --name ascend-backend --set-env-vars "FRONTEND_ORIGIN=https://$FrontendUrl"

Write-Host "Backend: https://$BackendUrl"
Write-Host "Frontend: https://$FrontendUrl"
Write-Host "Run migrations from a secure runner: alembic upgrade head"
