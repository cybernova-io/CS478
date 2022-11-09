import * as React from "react";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en.json";
import { Typography } from "@mui/material";

TimeAgo.addDefaultLocale(en);

export default function TimeDateAgo({ timeDate }) {
  const timeAgo = new TimeAgo("en-US");

  return (
    <Typography variant="caption">
      {timeAgo.format(new Date(timeDate))}
    </Typography>
  );
}
