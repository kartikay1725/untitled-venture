import React from 'react';

interface Props {
  data: { idea_id: string; validation_score: number; validated_at: string };
}

export default function ValidationResult({ data }: Props) {
  return (
    <div>
      <h2>Validation Score: {data.validation_score}%</h2>
      <p>Validated at: {new Date(data.validated_at).toLocaleString()}</p>
    </div>
  );
}