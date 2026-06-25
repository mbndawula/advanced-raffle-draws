# 🎡 Raffle Wheel Draw App

A fun Streamlit web app for conducting raffle draws where winners are selected based on weighted probability (more tickets = higher chance to win).

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


Alternatively:
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

The app creates an internal "ticket pool" where:

- If someone bought 5 tickets, their 5 numbers appear 5 times in the pool
- Random selection from this pool = person with more tickets has proportionally higher chance
- Still completely random - having 50 tickets doesn't guarantee a win

## Example

- Alice: 3 tickets (numbers 1, 2, 3)
- Bob: 2 tickets (numbers 4, 5)
- Total pool: [1, 2, 3, 4, 5]
- Alice has 3/5 = 60% chance, Bob has 2/5 = 40% chance
- But any single draw is random!
