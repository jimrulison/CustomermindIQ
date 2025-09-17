import React from 'react';
import { Helmet } from 'react-helmet-async';

const StructuredDataScript = ({ data }) => {
  if (!data) return null;
  
  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(data, null, 2)}
      </script>
    </Helmet>
  );
};

// Component for multiple structured data items
export const MultipleStructuredData = ({ dataArray }) => {
  if (!dataArray || !Array.isArray(dataArray)) return null;
  
  return (
    <Helmet>
      {dataArray.map((data, index) => (
        <script key={index} type="application/ld+json">
          {JSON.stringify(data, null, 2)}
        </script>
      ))}
    </Helmet>
  );
};

export default StructuredDataScript;