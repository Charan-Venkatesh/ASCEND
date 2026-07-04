declare module "next/navigation" {
  export function redirect(path: string): never;
  export function useRouter(): { push(path: string): void; replace(path: string): void; refresh(): void };
}
