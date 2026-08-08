import React from 'react';

interface Props {
  zipUrl: string;
}

export default function DownloadButton({ zipUrl }: Props) {
  return (
    <div>
      <a href={zipUrl} download>
        <button>Download MVP Package</button>
      </a>
    </div>
  );
}