import React, { useState } from 'react';
import axios from 'axios';

export default function Ideas() {
  const [description, setDescription] = useState('');
  const [score, setScore] = useState<number | null>(null);
  const [validatedAt, setValidatedAt] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const handleLogin = async () => {
    const res = await axios.post('/api/auth/login', {email: 'test@example.com', password: 'password123'});
    setToken(res.data.token);
  };

  const handleSubmit = async () => {
    const res = await axios.post('/api/ideas/', {description}, {headers: {Authorization: `Bearer ${token}`}});
    setScore(res.data.validation_score);
    setValidatedAt(res.data.validated_at);
  };

  return (
    <div>
      <h2>Idea Submission</h2>
      <textarea value={description} onChange={e => setDescription(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
      {score && <p>Score: {score}</p>}
      {validatedAt && <p>Validated At: {validatedAt}</p>}
    </div>
  );
}