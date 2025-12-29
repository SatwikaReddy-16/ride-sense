export function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  const num = Number(value);

  // Format using Indian locale + Add ₹ manually
  return "₹" + num.toLocaleString("en-IN", { maximumFractionDigits: 0 });
}

export function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  const num = Number(value);

  if (Math.abs(num) >= 1_000_000_000) return (num / 1_000_000_000).toFixed(1) + "B";
  if (Math.abs(num) >= 1_000_000) return (num / 1_000_000).toFixed(1) + "M";
  if (Math.abs(num) >= 1_000) return (num / 1_000).toFixed(1) + "K";
  
  return num.toString();
}
