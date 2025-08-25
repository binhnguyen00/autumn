import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import type { Root } from "react-dom/client"

import "./index.css"
import { App } from "./App.tsx"

const container: HTMLElement | null = document.getElementById("root");
if (container) {
  const root: Root = createRoot(container);
  root.render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
} else {
  throw Error("Root element not found");
}
