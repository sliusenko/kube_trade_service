function parseLookback(value) {
  if (!value) return null;
  const match = value.toString().match(/^(\d+)([smhd])$/i);
  if (!match) return parseInt(value, 10);

  const num = parseInt(match[1], 10);
  const unit = match[2].toLowerCase();
  switch (unit) {
    case "s": return num;
    case "m": return num * 60;
    case "h": return num * 3600;
    case "d": return num * 86400;
    default: return num;
  }
}

function formatLookback(seconds) {
  if (!seconds) return "";
  if (seconds % 86400 === 0) return (seconds / 86400) + "d";
  if (seconds % 3600 === 0) return (seconds / 3600) + "h";
  if (seconds % 60 === 0) return (seconds / 60) + "m";
  return seconds + "s";
}