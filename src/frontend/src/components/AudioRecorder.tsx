import { useState, useRef, useEffect } from 'react';
import { Button, Box, CircularProgress, Typography, Paper } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import SendIcon from '@mui/icons-material/Send';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import axios from 'axios';

const AudioRecorder = () => {
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
    <Paper
      elevation={3}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
        p: 4,
        width: '100%',
        maxWidth: 500,
        margin: '0 auto',
        borderRadius: 2,
        backgroundColor: 'background.paper'
      }}
    >
      <Typography variant="h4" component="h1" gutterBottom color="primary">
        Audio Recorder
      </Typography>

      {isRecording ? (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
            width: '100%'
          }}
        >
          <Box className="recording" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <FiberManualRecordIcon color="error" fontSize="large" />
            <Typography variant="h6" color="error">
              Recording...
            </Typography>
          </Box>
          <Typography variant="h4" color="primary">
            {formatTime(recordingTime)}
          </Typography>
          <Button
            variant="contained"
            color="error"
            onClick={stopRecording}
            startIcon={<StopIcon />}
            size="large"
            fullWidth
            sx={{ mt: 2 }}
          >
            Stop Recording
          </Button>
        </Box>
      ) : (
        <Button
          variant="contained"
          color="primary"
          onClick={startRecording}
          startIcon={<MicIcon />}
          disabled={isSending}
          size="large"
          fullWidth
          sx={{
            py: 2,
            fontSize: '1.1rem',
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #1565c0 30%, #00B0FF 90%)',
            },
          }}
        >
          {audioBlob ? 'Record Again' : 'Start Recording'}
        </Button>
      )}

      {audioBlob && !isRecording && (
        <Box sx={{ mt: 2, width: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Listen to your recording:
          </Typography>
          <audio
            controls
            src={URL.createObjectURL(audioBlob)}
            style={{ width: '100%', margin: '10px 0' }}
          />
          <Button
            variant="contained"
            color="success"
            onClick={sendAudioToBackend}
            disabled={isSending}
            startIcon={isSending ? <CircularProgress size={24} /> : <SendIcon />}
            size="large"
            fullWidth
            sx={{
              mt: 2,
              py: 1.5,
              fontSize: '1.1rem',
              background: 'linear-gradient(45deg, #2e7d32 30%, #4caf50 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1b5e20 30%, #2e7d32 90%)',
              },
            }}
          >
            {isSending ? 'Sending...' : 'Send to Server'}
          </Button>
        </Box>
      )}
    </Paper>
  );
};

export default AudioRecorder;
