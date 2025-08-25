import React from "react";
import axios from "axios";

export function AudioRecorder() {
  const [isRecording, setIsRecording] = React.useState(false);
  const [audioBlob, setAudioBlob] = React.useState<Blob | null>(null);
  const [isSending, setIsSending] = React.useState(false);
  const [recordingTime, setRecordingTime] = React.useState(0);
  const mediaRecorder = React.useRef<MediaRecorder | null>(null);
  const audioChunks = React.useRef<Blob[]>([]);
  const timerRef = React.useRef<number | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorder.current.onstop = () => {
        const audioBlob = new Blob(audioChunks.current, { type: "audio/wav" });
        setAudioBlob(audioBlob);
        if (timerRef.current !== null) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      setRecordingTime(0);

      const timerId = window.setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      timerRef.current = timerId;

    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Could not access microphone. Please ensure you have granted microphone permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const sendAudioToBackend = async () => {
    if (!audioBlob) return;

    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");

    try {
      setIsSending(true);
      const response = await axios.post("http://localhost:8080/api/audio", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Audio uploaded successfully:", response.data);
      alert("Audio sent successfully!");
      setAudioBlob(null);
      setRecordingTime(0);
    } catch (error) {
      console.error("Error uploading audio:", error);
      alert("Failed to send audio. Please try again.");
    } finally {
      setIsSending(false);
    }
  };

  React.useEffect(() => {
    return () => {
      if (mediaRecorder.current && isRecording) {
        mediaRecorder.current.stop();
      }
      if (timerRef.current !== null) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [isRecording]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="max-w-[500px] mx-auto p-5 text-center">
      <h2 className="text-2xl font-bold mb-6">Audio Recorder</h2>

      {!isRecording && !audioBlob && (
        <button
          onClick={startRecording}
          className="px-5 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors mt-5"
        >
          Start Recording
        </button>
      )}

      {isRecording && (
        <div className="my-5">
          <div className="w-5 h-5 bg-red-500 rounded-full inline-block my-2.5 animate-pulse"></div>
          <p className="my-2">Recording: {formatTime(recordingTime)}</p>
          <button
            onClick={stopRecording}
            className="px-5 py-2.5 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors mt-2.5"
          >
            Stop Recording
          </button>
        </div>
      )}

      {audioBlob && !isRecording && (
        <div className="my-5">
          <p className="mb-2">Recording complete! ({formatTime(recordingTime)})</p>
          <audio
            src={URL.createObjectURL(audioBlob)}
            controls
            className="w-full my-5"
          />
          <div className="flex gap-2.5 justify-center mt-5">
            <button
              onClick={() => setAudioBlob(null)}
              disabled={isSending}
              className="px-4 py-2 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Discard
            </button>
            <button
              onClick={sendAudioToBackend}
              disabled={isSending}
              className={`px-4 py-2 rounded-md text-white transition-colors ${isSending ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                }`}
            >
              {isSending ? "Sending..." : "Send"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};