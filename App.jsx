import React, { useState } from 'react';

const App = () => {
  const [tone, setTone] = useState('Neutral');
  const [language, setLanguage] = useState('');
  const [inputType, setInputType] = useState('');
  const [isPremium, setIsPremium] = useState(false);
  const [signedIn, setSignedIn] = useState(false);

  const handleSignIn = () => {
    setSignedIn(true);
    speak(`Signed in successfully in ${language}`);
  };

  const handleGoBack = () => {
    setSignedIn(false);
    setLanguage('');
    speak('Returning to language selection');
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'Tamil' ? 'ta-IN' : language === 'Hindi' ? 'hi-IN' : 'en-US';
    speechSynthesis.speak(utterance);
  };

  return (
    <div style={styles.app}>
      {!signedIn ? (
        <div style={styles.signin}>
          <h2>Select Language</h2>
          <div style={styles.languageRow}>
            {['English', 'Tamil', 'Hindi'].map((lang) => (
              <button
                key={lang}
                style={styles.langBtn}
                onClick={() => {
                  setLanguage(lang);
                  speak(`Language selected: ${lang}`);
                }}
              >
                {lang === 'English' ? '🇬🇧' : '🇮🇳'} {lang}
              </button>
            ))}
          </div>
          <button style={styles.signinBtn} onClick={handleSignIn}>
            🔊 Audio-Guided Sign-In
          </button>
        </div>
      ) : (
        <div style={styles.main}>
          <h1>Welcome, {language} User!</h1>

          {/* Go Back Button */}
          <button style={styles.goBackBtn} onClick={handleGoBack}>
            🔙 Go Back
          </button>

          {/* Input Icons */}
          <div style={styles.section}>
            <h3>Select Input Type</h3>
            <div style={styles.iconRow}>
              {['Text', 'File', 'Image', 'Voice'].map((type) => (
                <button
                  key={type}
                  style={styles.iconBtn}
                  onClick={() => {
                    setInputType(type);
                    speak(`${type} input selected`);
                  }}
                >
                  {type === 'Text' && '📝'}
                  {type === 'File' && '📁'}
                  {type === 'Image' && '🖼️'}
                  {type === 'Voice' && '🎤'}
                  <br />
                  {type}
                </button>
              ))}
            </div>
          </div>

          {/* Tone Selection */}
          <div style={styles.section}>
            <h3>Select Tone</h3>
            {['Neutral', 'Suspenseful', 'Inspiring'].map((t) => (
              <label key={t} style={styles.radioLabel}>
                <input
                  type="radio"
                  value={t}
                  checked={tone === t}
                  onChange={() => {
                    setTone(t);
                    speak(`Tone set to ${t}`);
                  }}
                />
                {t}
              </label>
            ))}
          </div>

          {/* Output Screen */}
          <div style={styles.section}>
            <h3>Output</h3>
            <button style={styles.outBtn} onClick={() => speak('Playing output')}>▶️ Play</button>
            <button style={styles.outBtn}>⬇️ Download</button>
            <button style={styles.outBtn}>🔗 Share</button>
          </div>

          {/* Premium/Freemium UI */}
          <div style={styles.section}>
            <h3>Access Mode</h3>
            <label style={styles.radioLabel}>
              <input
                type="checkbox"
                checked={isPremium}
                onChange={() => {
                  setIsPremium(!isPremium);
                  speak(isPremium ? 'Switched to Freemium' : 'Premium features enabled');
                }}
              />
              {isPremium ? 'Premium Features Enabled' : 'Freemium Mode'}
            </label>
          </div>

          {/* Step-by-Step Visual Flow */}
          <div style={styles.section}>
            <h3>Step-by-Step Guidance</h3>
            {[1, 2, 3].map((step) => (
              <button
                key={step}
                style={styles.visualBtn}
                onClick={() => speak(`Step ${step} activated`)}
              >
                🔊 Step {step}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// 🎨 Inline Styles
const styles = {
  app: {
    fontFamily: 'Segoe UI, sans-serif',
    background: 'linear-gradient(to right, #e0f7fa, #fce4ec)',
    minHeight: '100vh',
    padding: '20px',
    color: '#333',
    textAlign: 'center',
  },
  signin: {
    marginTop: '50px',
  },
  languageRow: {
    display: 'flex',
    justifyContent: 'center',
    gap: '15px',
    marginBottom: '20px',
  },
  langBtn: {
    padding: '15px 20px',
    fontSize: '1.2em',
    borderRadius: '10px',
    border: 'none',
    backgroundColor: '#fff',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    cursor: 'pointer',
  },
  signinBtn: {
    backgroundColor: '#ffccbc',
    fontSize: '1.2em',
    padding: '15px 30px',
    borderRadius: '10px',
    border: 'none',
    cursor: 'pointer',
  },
  goBackBtn: {
    backgroundColor: '#ffe082',
    fontSize: '1em',
    padding: '10px 20px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    marginBottom: '20px',
  },
  main: {
    marginTop: '30px',
  },
  section: {
    margin: '30px 0',
  },
  iconRow: {
    display: 'flex',
    justifyContent: 'center',
    gap: '15px',
    flexWrap: 'wrap',
  },
  iconBtn: {
    padding: '15px',
    fontSize: '1.1em',
    borderRadius: '10px',
    border: 'none',
    backgroundColor: '#fff',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    width: '100px',
  },
  radioLabel: {
    margin: '10px',
    fontSize: '1.1em',
  },
  outBtn: {
    margin: '10px',
    padding: '10px 20px',
    fontSize: '1em',
    borderRadius: '8px',
    border: 'none',
    backgroundColor: '#e1bee7',
    cursor: 'pointer',
  },
  visualBtn: {
    margin: '10px',
    padding: '15px 25px',
    fontSize: '1.1em',
    borderRadius: '12px',
    border: 'none',
    backgroundColor: '#c8e6c9',
    cursor: 'pointer',
  },
};

export default App;