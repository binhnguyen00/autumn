import React from "react";
import { webSocketService } from "../services/websocket";

export function AudioRecorder() {
  const [isRecording, setIsRecording] = React.useState(false);
  const [recordingTime, setRecordingTime] = React.useState(0);
  const [transcript, setTranscript] = React.useState<string>("");
  const [status, setStatus] = React.useState<string>("");
  const mediaRecorder = React.useRef<MediaRecorder | null>(null);
  const timerRef = React.useRef<number | null>(null);

  const startRecording = async () => {
    try {
      setTranscript("");
      setStatus("Connecting...");

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);

      mediaRecorder.current.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          webSocketService.sendAudio(event.data);
        }
      };

      // Set up WebSocket listeners
      const onTranscript = (data: any) => {
        if (data.text) setTranscript(prev => prev + ' ' + data.text);
      };

      const onStatus = (data: any) => {
        if (data.message) setStatus(data.message);
      };

      webSocketService.on('transcript', onTranscript);
      webSocketService.on('status', onStatus);

      // Start recording with small timeslice for real-time streaming
      mediaRecorder.current.start(100);
      setIsRecording(true);
      setStatus('Recording...');
      setRecordingTime(0);

      const timerId = window.setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      timerRef.current = timerId;

      return () => {
        webSocketService.off('transcript', onTranscript);
        webSocketService.off('status', onStatus);
      };
    } catch (error) {
      console.error("Error accessing microphone:", error);
      setStatus("Error accessing microphone");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
      setStatus('Recording stopped');
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

      {!isRecording ? (
        <button
          onClick={startRecording}
          className="px-5 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors mt-5"
        >
          Start Recording
        </button>
      ) : (
        <div className="my-5">
          <div className="w-5 h-5 bg-red-500 rounded-full inline-block my-2.5 animate-pulse"></div>
          <p className="my-2">Recording: {formatTime(recordingTime)}</p>
          <p className="text-sm text-gray-600">{status}</p>
          <button
            onClick={stopRecording}
            className="px-5 py-2.5 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors mt-2.5"
          >
            Stop Recording
          </button>
        </div>
      )}

      {transcript && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg text-left">
          <h3 className="font-semibold mb-2">Transcript:</h3>
          <p className="whitespace-pre-wrap">{transcript}</p>
        </div>
      )}
    </div>
  );
};