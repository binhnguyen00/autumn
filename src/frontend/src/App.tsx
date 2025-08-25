import { AudioRecorder } from "./components/AudioRecorder";

export function App() {
  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      backgroundColor: "#f5f5f5",
      fontFamily: "Arial, sans-serif"
    }}>
      <AudioRecorder />
    </div>
  );
};