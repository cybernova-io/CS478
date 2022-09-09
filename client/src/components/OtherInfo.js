import React from "react";

function OtherInfo({ formData, setFormData }) {
  return (
    <div className="other-info-container">
      <input
        type="text"
        placeholder="Major..."
        value={formData.major}
        onChange={(e) => {
          setFormData({ ...formData, major: e.target.value });
        }}
      />
      <input
        type="text"
        placeholder="Graduation Year..."
        value={formData.gradYear}
        onChange={(e) => {
          setFormData({ ...formData, other: e.target.value });
        }}
      />
    </div>
  );
}

export default OtherInfo;
