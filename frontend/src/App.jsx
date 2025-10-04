import { useState } from 'react'
import { useEffect } from 'react'
import './App.css'


export default function App() {
  //const [count, setCount] = useState(0);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasTyped, setHasTyped] = useState(false);
  const [hasSent, setHasSent] = useState(false);




  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    const userMessage = {role: 'user', content: input};
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setHasSent(true);

    try {

      const response = await fetch('http://127.0.0.1:8000/chat', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ message: userMessage.content })
       });

       if (!response.ok) throw new Error(`HTTP ${response.status}`);
       const data = await response.json();
       const assistantMessage = { role: 'assistant', content: data.reply };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, there was an error processing your request.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const endChat = async () => {
    setIsLoading(true);
    try {
      await fetch('http://127.0.0.1:8000/reset', { method: 'POST' });
    } catch (e) {
      console.error(e);
    } finally {
      // Clear UI state
      setMessages([]);
      setInput('');
      setHasSent(false);
      setHasTyped(false);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const onEsc = (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        endChat();   
      }
    };
    window.addEventListener('keydown', onEsc);
    return () => window.removeEventListener('keydown', onEsc);
  }, [endChat]);

  

  

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      padding: '20px',
      gap: '10px',
      maxWidth: '100%',
      margin: '0 auto',
      backgroundColor: messages.length === 0 ? '#f9fafb' : 'transparent',

      // Once the user has sent message
      width: hasSent ? undefined: '100vh',

    position: hasSent ? 'fixed' : 'static',
    left: hasSent ? 0 : undefined,
    right: hasSent ? 0 : undefined,
    bottom: hasSent ? 0: undefined,
    marginRight: hasSent ? '0px' : '2px',
    padding: hasSent ? '10px':'20px'


    }}>


      {/* Message display */}

      <div style={{
        flex: 1,
        overflowY: 'auto',
        marginBottom: '20px',
        padding: '5px 20px',
        paddingTop: '50px',
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        maxHeight: '600px',
      }}>
            {messages.length === 0 && (
              <div style={{ marginBottom: '0px'}}>
                <h1 style={{
                  fontWeight: 'bold',
                  fontSize: '36x',
                  color: '#333',
                  marginBottom: '5px',
                  textAlign:'center'

                }} >
                  MedAssist AI
                  
                </h1>
                <p style={{ color: '#999', fontSize: '20px', textAlign: 'center', marginTop:'0px' }}>
                  How are you feeling today?
                </p>
            

              </div>

        )}


        
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              display: 'flex',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start', 
              padding: '0 10px',
              marginBottom: '12px',
              width: '100%',
            }}
          >
            <div
              style={{
                backgroundColor: msg.role === 'user' ? '#007bff' : '#f0f0f0',
                color: msg.role === 'user' ? 'white' : 'black',
                padding: '12px',
                borderRadius: '12px',
                maxWidth: '85%',
                whiteSpace: 'pre-wrap',
                lineHeight: 1.4,
              }}
          
 
          >
            {msg.content}
          </div>
        </div>
      ))}

        {isLoading && (
          <div className="typing-row">
            <div className="typing-bubble">
              <span className="typing-dots" />
            </div>
          </div>
        )}



        
      </div>

      {/* Input and Send Button */}

      <div style={{
        display: 'flex',
        gap: '10px',
        padding: '0px 15px',
        marginLeft: '10px'

      }}
      >

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          style={{
            flex: 5,
            padding: '14px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius:'8px',

          }}
        />

        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          style={{
            padding: '12px 24px',
            backgroundColor: input.trim() ? '#007bff' : '#ccc',
           // boxSizing: 'border-box',
            color: 'white',
            borderRadius: '8px',
            cursor: input.trim() ? 'pointer' : 'not-allowed'
          }}
        >
          {'\u21B5'}
        </button>
      </div>

      <footer style={{
        textAlign: 'center',
        fontSize: '10px',
        color: '#888',
        marginTop: '30px',
        paddingBottom: '10px',
        fontFamily: 'Verdana, sans-serif'
      }}>
        © {new Date().getFullYear()} Made by Andrea Cardiel
      </footer>




    </div>

  );



}
