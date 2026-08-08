import { useState } from 'react';
import axios from 'axios';

interface Props {
  onSubmit: (data: any) => void;
}

export default function IdeaForm({ onSubmit }: Props) {
  const [description, setDescription] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/ideas`, { description });
    onSubmit(res.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Describe your idea"
        required
      />
      <button type="submit">Validate Idea</button>
    </form>
  );
}