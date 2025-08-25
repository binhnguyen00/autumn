import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import AudioRecorder from './components/AudioRecorder';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
        <AudioRecorder />
      </div>
    </ThemeProvider>
  );
}

export default App;
