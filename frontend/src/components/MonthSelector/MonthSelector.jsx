// frontend/src/components/MonthSelector/MonthSelector.jsx
import React, { useEffect, useState } from "react";
import styles from "./MonthSelector.module.css";

const months = [
  { name: "Jan", value: 1 },
  { name: "Feb", value: 2 },
  { name: "Mar", value: 3 },
  { name: "Apr", value: 4 },
  { name: "May", value: 5 },
  { name: "Jun", value: 6 },
  { name: "Jul", value: 7 },
  { name: "Aug", value: 8 },
  { name: "Sep", value: 9 },
  { name: "Oct", value: 10 },
  { name: "Nov", value: 11 },
  { name: "Dec", value: 12 },
];

export default function MonthSelector({ year, month, onChange }) {
  // local controlled values so changes only apply when user clicks "Apply"
  const [tempYear, setTempYear] = useState(year === "" ? "" : String(year ?? ""));
  const [tempMonth, setTempMonth] = useState(month === "" ? "" : String(month ?? ""));

  useEffect(() => {
    // keep local inputs in sync if parent updates selected externally
    setTempYear(year === "" ? "" : String(year ?? ""));
    setTempMonth(month === "" ? "" : String(month ?? ""));
  }, [year, month]);

  function handleMonthSelect(e) {
    setTempMonth(e.target.value);
  }

  function handleYearInput(e) {
    setTempYear(e.target.value);
  }

  function applySelection() {
    // pass year as string (to preserve user's typing) and month as number or ""
    const y = tempYear === "" ? "" : tempYear;
    const m = tempMonth === "" ? "" : Number(tempMonth);
    onChange(y, m);
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      applySelection();
    }
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.box}>
        <label className={styles.label}>Month</label>
        <select
          value={tempMonth || ""}
          onChange={handleMonthSelect}
          className={styles.select}
        >
          <option value="">Select</option>
          {months.map((m) => (
            <option key={m.value} value={m.value}>
              {m.name}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.box}>
        <label className={styles.label}>Year</label>
        <input
          type="text"
          placeholder="YYYY"
          className={styles.input}
          value={tempYear}
          onChange={handleYearInput}
          onKeyDown={onKeyDown}
          inputMode="numeric"
        />
      </div>

      <div className={styles.box} style={{ alignSelf: "flex-end" }}>
        <button
          type="button"
          className={styles.applyBtn}
          onClick={applySelection}
        >
          Apply
        </button>
      </div>
    </div>
  );
}
