import { create } from 'zustand';

type AppState = {
  activeCollectionId?: string;
  setActiveCollectionId: (id?: string) => void;
};

export const useAppStore = create<AppState>((set) => ({
  activeCollectionId: undefined,
  setActiveCollectionId: (id) => set({ activeCollectionId: id }),
}));
