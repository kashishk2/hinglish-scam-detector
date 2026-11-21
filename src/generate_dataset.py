"""
Generates a synthetic Hinglish scam/safe SMS dataset -> data/raw_messages.csv
Run from project root:  python src/generate_dataset.py
Columns: text, label (1 = scam, 0 = safe), category
"""
import random
import pandas as pd

random.seed(42)

def pick(x):
    return random.choice(x)

def fill(template):
    """Replace {slots} in a template with random values."""
    slots = {
        "bank": ["SBI", "HDFC", "ICICI", "PNB", "Axis Bank", "Kotak", "Bank of Baroda", "Canara Bank"],
        "amt": ["5000", "10000", "25000", "50000", "1,00,000", "2,50,000", "5 lakh", "10 lakh"],
        "small_amt": ["199", "499", "749", "1200", "2500", "3400"],
        "url": ["bit.ly/kyc-upd8", "http://sbi-kyc-update.in", "tinyurl.com/claim-now", "http://hdfc-secure.xyz/login",
                "bit.ly/3xYzAb", "http://paytm-rewards.top", "https://upi-refund.info", "http://jio-offer.click"],
        "num": ["9876543210", "8800112233", "7011223344", "9123456789", "6290001122"],
        "app": ["PhonePe", "Paytm", "Google Pay", "BHIM", "Amazon Pay"],
        "name": ["Rahul", "Amit", "Priya", "Neha", "Karan", "Simran", "Gurpreet", "Rohan", "Anjali", "Harpreet"],
        "hrs": ["24", "12", "6", "2", "48"],
        "otp": ["482913", "731905", "260847", "559012", "904376", "118264"],
        "acct": ["XX4821", "XX7305", "XX1196", "XX9042", "XX6638"],
        "brand": ["Amazon", "Flipkart", "Myntra", "Zomato", "Swiggy", "Meesho"],
        "city": ["Ludhiana", "Delhi", "Chandigarh", "Jalandhar", "Amritsar", "Pune", "Mumbai"],
        "time": ["5 baje", "6:30", "shaam ko", "kal subah", "10 baje", "raat ko 8 baje"],
        "company": ["Amazon", "TCS", "Infosys", "Google", "Flipkart", "Wipro"],
    }
    out = template
    for k, v in slots.items():
        while "{" + k + "}" in out:
            out = out.replace("{" + k + "}", pick(v), 1)
    return out

SCAM = {
    "fake_kyc": [
        "Dear customer, aapka {bank} account KYC expire ho gaya hai. Abhi update karein warna account block ho jayega: {url}",
        "{bank} Alert: Aapka KYC pending hai. {hrs} ghante mein update nahi kiya toh account band ho jayega. Click karo {url}",
        "URGENT: Aapka PAN card {bank} account se link nahi hai. Turant link karein {url}",
        "Dear user aapka {bank} net banking aaj raat block hoga. KYC verify karne ke liye call karo {num}",
        "Aapka {bank} debit card band hone wala hai. Details update karo yahan: {url}",
        "KYC update nahi kiya? Aapka account freeze ho sakta hai. Abhi verify karein {url} - {bank}",
    ],
    "lottery": [
        "Congratulations! Aapne {amt} rupaye ki lottery jeeti hai. Claim karne ke liye {url} par click karein",
        "Badhai ho! Aapka number KBC lucky draw mein select hua hai, Rs {amt} jeetne ke liye call karo {num}",
        "Aapko {brand} ki taraf se free iPhone mila hai! Abhi claim karo {url}, offer {hrs} ghante mein khatam",
        "You have won Rs {amt}! Apna prize lene ke liye processing fee {small_amt} bhejo {app} par {num}",
        "Jio lucky draw winner! Aapne {amt} jeeta hai. Apni details bhejo {url}",
        "Mubarak ho! {brand} anniversary lucky draw mein aap winner hain. Gift pane ke liye register karo {url}",
    ],
    "upi_refund": [
        "Aapka {app} refund of Rs {small_amt} pending hai. Receive karne ke liye UPI PIN enter karein {url}",
        "Sir galti se aapke account mein Rs {amt} aa gaye hain, please wapas bhej do {num} par {app} se",
        "{app} cashback Rs {small_amt} mila hai! Collect karne ke liye request accept karein aur PIN daalein",
        "Aapka payment fail ho gaya, refund ke liye apna UPI PIN aur card details share karein {url}",
        "Refund process karne ke liye AnyDesk download karein aur code humein batayein. Call {num}",
        "Dear customer, {app} wallet mein Rs {amt} credit hone wale hain. Verify karne ke liye {url} par login karein",
    ],
    "fake_job": [
        "Work from home job! Roz Rs {small_amt} kamao, sirf mobile chahiye. WhatsApp karo {num}",
        "{company} mein urgent hiring. Registration fee Rs {small_amt} {app} karo aur offer letter pao. Contact {num}",
        "Part time job offer: YouTube videos like karo aur har like pe Rs 50 kamao. Join karo {url}",
        "Congratulations aapka resume {company} ke liye shortlist hua hai. Training fee Rs {small_amt} jama karein {url}",
        "Ghar baithe Rs {amt} mahina kamao! Koi experience nahi chahiye. Telegram par msg karo {num}",
        "Data entry job available, salary Rs 30000/month. Pehle security deposit Rs {small_amt} bhejein",
    ],
    "otp_phishing": [
        "Main {bank} se bol raha hoon, aapke account mein problem hai. Abhi OTP bataiye jo aapko aaya hai",
        "Aapka {bank} account verify karne ke liye OTP share karein, warna account suspend ho jayega. Call {num}",
        "Dear customer, aapke card se Rs {amt} deduct hue hain. Cancel karne ke liye OTP aur CVV batayein {num}",
        "{bank} Security: Unauthorized login detected. Apna OTP aur PIN is link par daalein {url}",
        "Aapka SIM {hrs} ghante mein block hoga. Verify karne ke liye Aadhaar aur OTP bhejein {url}",
    ],
    "utility_threat": [
        "Dear consumer, aapka bijli bill pending hai, aaj raat 9:30 baje connection kat jayega. Abhi call karein {num}",
        "PSPCL Alert: Last month ka bill update nahi hua. Turant {url} par payment karo warna connection cut",
        "Aapka gas connection band hone wala hai. KYC update karne ke liye {num} par contact karein",
        "Aapke naam se ek parcel customs mein ruka hai. Release karne ke liye Rs {small_amt} bhejo {url}",
        "Traffic challan Rs {small_amt} pending hai. Abhi pay karein {url} warna court notice aayega",
    ],
    "loan_fraud": [
        "Instant loan Rs {amt} sirf 5 minute mein! Koi documents nahi chahiye. Apply karo {url}",
        "Pre-approved personal loan Rs {amt}. Processing fee Rs {small_amt} pehle bhejein. Call {num}",
        "Aapka loan approve ho gaya hai! Disbursement ke liye insurance charge Rs {small_amt} jama karein {url}",
        "Low CIBIL? No problem! Guaranteed loan Rs {amt}. Aaj hi apply karo {url}",
    ],
}

SAFE = {
    "friends_family": [
        "Bhai kal {time} milte hain, {city} wale cafe mein",
        "Mummy ne kaha hai ki aaj ghar jaldi aana, mehmaan aa rahe hain",
        "Oye {name}, assignment submit kar diya kya? Mera abhi baaki hai yaar",
        "Happy birthday {name}! Party kab de raha hai? Treat toh banti hai",
        "Yaar mera phone charge nahi ho raha, tu {time} call kar lena",
        "Kal ka match dekha? Kya zabardast khela yaar!",
        "Papa ka call aaya tha, bol rahe the sunday ko {city} jaana hai",
        "Bro notes bhej de DBMS ke, kal exam hai aur maine kuch nahi padha",
        "Chal dinner pe chalte hain aaj, tu bata kahan jana hai",
        "Thik hai bhai, main {time} tak pahunch jaunga. Tension mat le",
        "Aaj lecture cancel ho gaya, library mein mil {name}",
        "Sorry yaar late ho gaya, traffic bahut tha. 10 min mein pahunch raha hoon",
    ],
    "bank_alert": [
        "Rs {small_amt} debited from a/c {acct} on UPI. Not you? Call bank helpline. -{bank}",
        "Rs {amt} credited to your a/c {acct}. Avl bal Rs {amt}. -{bank}",
        "Your {bank} statement for this month is ready. Login to the official app to view.",
        "Dear customer, your debit card ending 4821 was used for Rs {small_amt} at a merchant. -{bank}",
        "Aapke {bank} account {acct} mein Rs {small_amt} credit hue hain. Dhanyavaad.",
        "Reminder: Aapki credit card ka payment due date kal hai. Please pay via official {bank} app.",
    ],
    "legit_otp": [
        "{otp} is your OTP for {app} login. Do not share it with anyone.",
        "Your OTP for {brand} order is {otp}. Valid for 10 minutes. Kisi ke saath share na karein.",
        "{otp} aapka {bank} transaction OTP hai. Ise kisi ko na batayein, bank kabhi nahi puchta.",
        "Use {otp} to verify your {brand} account. Never share this code.",
    ],
    "delivery_orders": [
        "Aapka {brand} order kal tak deliver ho jayega. Track karein app mein.",
        "Your {brand} order has been shipped. Delivery partner aaj {time} tak pahunchega.",
        "Delivery agent {name} aapke ghar ke bahar hai, kripya gate pe aaiye.",
        "Aapka {brand} refund Rs {small_amt} original payment method mein 3-5 din mein aa jayega.",
        "Order delivered! Humein batayein aapko kaisa laga. Rate karein {brand} app mein.",
    ],
    "work_college": [
        "Meeting {time} shift ho gayi hai, please calendar check kar lena.",
        "Sir, project report kal tak submit kar dunga. Thoda aur time mil sakta hai?",
        "Reminder: Kal 10 baje se mid-sem exams shuru hain. Admit card collect kar lein.",
        "Aapka interview {company} ke saath {time} schedule hua hai. Confirm karne ke liye reply karein.",
        "Placement cell: Kal campus drive hai, formal dress mein aana aur resume ki 2 copies laana.",
        "Team, aaj ka standup {time} hoga. Sab log join karna please.",
        "Hostel mess ka timing badal gaya hai, ab dinner 8 baje se hoga.",
    ],
    "services_promo": [
        "Aapka recharge Rs {small_amt} successful raha. Validity 28 din. Thank you for choosing us.",
        "Aapka {app} par Rs {small_amt} ka payment {name} ko successful hua.",
        "Your appointment with Dr. Sharma is confirmed for {time}. Please arrive 10 min early.",
        "Flight reminder: aapki flight kal subah {city} ke liye hai. Web check-in kar lein.",
        "Aapki library book kal due hai. Late fee se bachne ke liye return kar dein.",
    ],
}

def build(per_scam=40, per_safe=45):
    rows = []
    for cat, templates in SCAM.items():
        for _ in range(per_scam):
            rows.append((fill(pick(templates)), 1, cat))
    for cat, templates in SAFE.items():
        for _ in range(per_safe):
            rows.append((fill(pick(templates)), 0, cat))
    return rows

def add_noise(text):
    """Simulate real-life messy typing: casing, spelling variants."""
    swaps = {"aapka": ["apka", "aapka", "aap ka"], "karein": ["karen", "karein", "kare"],
             "abhi": ["abhi", "abi", "abhi"], "hai": ["hai", "h", "hai"],
             "warna": ["warna", "varna", "warna"], "turant": ["turant", "turat", "turant"],
             "account": ["account", "acc", "a/c"], "ghante": ["ghante", "ghnte", "ghante"]}
    words = text.split()
    for i, w in enumerate(words):
        lw = w.lower().strip(".,!:")
        if lw in swaps and random.random() < 0.35:
            words[i] = pick(swaps[lw])
    text = " ".join(words)
    r = random.random()
    if r < 0.12:
        text = text.upper()
    elif r < 0.25:
        text = text.lower()
    return text

if __name__ == "__main__":
    rows = build()
    df = pd.DataFrame(rows, columns=["text", "label", "category"])
    df["text"] = df["text"].apply(add_noise)
    df = df.drop_duplicates(subset="text").sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv("data/raw_messages.csv", index=False, encoding="utf-8")
    print(f"Saved {len(df)} messages -> data/raw_messages.csv")
    print(df["label"].value_counts().rename({1: "scam", 0: "safe"}))
    print("\nBy category:\n", df["category"].value_counts())