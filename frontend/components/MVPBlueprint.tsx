import { useState } from 'react';
import axios from 'axios';

interface Props {
  ideaId: string;
  onGenerate: (data: any) => void;
}

export default function MVPBlueprint({ ideaId, onGenerate }: Props) {
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    setGenerating(true);
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/mvp`, { idea_id: ideaId });
    onGenerate(res.data);
    setGenerating(false);
  };

  return (
    <div>
      <button onClick={handleGenerate} disabled={generating}>
        {generating ? 'Generating...' : 'Generate MVP Blueprint'}
      </button>
    </div>
  );
}