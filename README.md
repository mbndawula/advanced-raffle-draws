# 🎡 Raffle Wheel Draw App

A fun web app for conducting raffle draws of all sorts! More tickets = higher chance to win!

## Features

✨ **Visual Spinning Wheel** - Animated number reveal for excitement
🎯 **Weighted Probability** - People with more tickets have better odds
🏆 **Winner Display** - Shows ticket number and winner name
📊 **Live Statistics** - See all participants and their odds
📜 **Draw History** - Track all winners in the session

## How It Works

1. **Public Display**: The wheel spins and reveals a "winning ticket number"
2. **Behind the Scenes**: The system randomly selects from a pool of all ticket numbers, where each person's numbers appear once for each ticket they bought
3. **Result**: Fair, transparent, but with weighted odds based on participation

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run raffle_app.py
```

### 3. Alternatively run the app using:
```bash
python -m streamlit run raffle_app.py
```

The app will open in your browser at `http://localhost:8501`

## File Structure

- `Raffle_26Jun26.xlsx` - Your raffle ticket data (Name, Ticket Count, Numbers)
- `raffle_app.py` - The Streamlit application
- `requirements.txt` - Python dependencies

## How to Use

1. Open the app in your browser
2. Click **"🎰 SPIN THE WHEEL!"** button
3. Watch the animated wheel spin
4. See the winning ticket number and the winner's name displayed
5. Repeat as many times as you want
6. Draw history is tracked during the session

## Probability Logic

The app creates a highly advanced internal logic pool.

## Example

- Nah.
