export function validateUpi(upiId) {
  if (!upiId?.trim()) return "UPI ID is required";
  if (!/^[a-zA-Z0-9._-]{2,}@[a-zA-Z]{2,}$/.test(upiId.trim())) {
    return "Use format: name@paytm or name@ybl";
  }
  return null;
}

export function validateCard({ cardNumber, cardName, expiry, cvv }) {
  const digits = (cardNumber || "").replace(/\D/g, "");
  if (digits.length < 13) return "Enter a valid card number";
  if (!cardName?.trim() || cardName.trim().length < 2) return "Name on card is required";
  if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test((expiry || "").trim())) return "Expiry must be MM/YY";
  if (!/^\d{3,4}$/.test((cvv || "").trim())) return "CVV must be 3–4 digits";
  return null;
}

export function calcEmi(total, months) {
  const monthly = Math.round((total / months) * 100) / 100;
  return { emi_months: months, months, monthly_amount: monthly, monthly, total };
}
