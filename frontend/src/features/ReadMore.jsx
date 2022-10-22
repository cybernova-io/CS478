import * as React from "react";
import Typography from "@mui/material/Typography";
import { useState } from "react";

export default function ReadMore({ children }) {
  const text = children;
  const [isReadMore, setIsReadMore] = useState(true);
  const toggleReadMore = () => {
    setIsReadMore(!isReadMore);
  };
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      sx={{ whiteSpace: "pre-line" }}
    >
      {isReadMore ? text.slice(0, 40) : text}
      <br />
      <span
        onClick={toggleReadMore}
        className="read-or-hide"
        style={{ color: "#062343", cursor: "pointer" }}
      >
        {isReadMore && text.length > 40 ? "...read more" : ""}
      </span>
    </Typography>
  );
}
89;
frontend / components / post / CommentForm.jsx;
