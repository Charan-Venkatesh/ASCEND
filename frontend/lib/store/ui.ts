import { create } from "zustand";

type UIState = {
  sidebarOpen: boolean;
  mentorMode: "mentor" | "strict" | "review";
  draftReflection: string;
  setSidebarOpen: (value: boolean) => void;
  setMentorMode: (value: UIState["mentorMode"]) => void;
  setDraftReflection: (value: string) => void;
};

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  mentorMode: "mentor",
  draftReflection: "",
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setMentorMode: (mentorMode) => set({ mentorMode }),
  setDraftReflection: (draftReflection) => set({ draftReflection })
}));
