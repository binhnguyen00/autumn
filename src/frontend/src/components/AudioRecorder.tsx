import axios from 'axios';

import { useState, useRef, useEffect } from 'react';

export function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

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
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
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
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please ensure you have granted microphone permissions.');
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
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      setIsSending(true);
      const response = await axios.post('http://localhost:8080/api/audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Audio uploaded successfully:', response.data);
      alert('Audio sent successfully!');
      setAudioBlob(null);
      setRecordingTime(0);
    } catch (error) {
      console.error('Error uploading audio:', error);
      alert('Failed to send audio. Please try again.');
    } finally {
      setIsSending(false);
    }
  };

  useEffect(() => {
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
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px', textAlign: 'center' }}>
      <h2>Audio Recorder</h2>

      {!isRecording && !audioBlob && (
        <button
          onClick={startRecording}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginTop: '20px'
          }}
        >
          Start Recording
        </button>
      )}

      {isRecording && (
        <div style={{ margin: '20px 0' }}>
          <div style={{
            width: '20px',
            height: '20px',
            backgroundColor: 'red',
            borderRadius: '50%',
            display: 'inline-block',
            margin: '10px 0',
            animation: 'pulse 1.5s infinite'
          }}></div>
          <p>Recording: {formatTime(recordingTime)}</p>
          <button
            onClick={stopRecording}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#dc004e',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '10px'
            }}
          >
            Stop Recording
          </button>
        </div>
      )}

      {audioBlob && !isRecording && (
        <div style={{ margin: '20px 0' }}>
          <p>Recording complete! ({formatTime(recordingTime)})</p>
          <audio
            src={URL.createObjectURL(audioBlob)}
            controls
            style={{ width: '100%', margin: '20px 0' }}
          />
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
            <button
              onClick={() => setAudioBlob(null)}
              disabled={isSending}
              style={{
                padding: '8px 16px',
                fontSize: '14px',
                backgroundColor: '#f5f5f5',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Discard
            </button>
            <button
              onClick={sendAudioToBackend}
              disabled={isSending}
              style={{
                padding: '8px 16px',
                fontSize: '14px',
                backgroundColor: isSending ? '#ccc' : '#1976d2',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: isSending ? 'not-allowed' : 'pointer'
              }}
            >
              {isSending ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};