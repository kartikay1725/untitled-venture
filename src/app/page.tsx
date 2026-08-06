import IdeaForm from '@/components/IdeaForm';
import ValidationCard from '@/components/ValidationCard';
import MVPBlueprint from '@/components/MVPBlueprint';
import { useState } from 'react';

export default function Home() {
  const [ideaId, setIdeaId] = useState<string | null>(null);
  const [blueprintId, setBlueprintId] = useState<string | null>(null);

  return (
    <div className="space-y-8">
      <IdeaForm onSuccess={(id) => setIdeaId(id)} />
      {ideaId && <ValidationCard ideaId={ideaId} onBlueprintGenerated={(id) => setBlueprintId(id)} />}
      {blueprintId && <MVPBlueprint blueprintId={blueprintId} />}
    </div>
  );
}
