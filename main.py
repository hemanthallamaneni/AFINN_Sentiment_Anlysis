"""
Hemanth Allamaneni  
EPPS 6317 Final Project
This is a sentiment analysis application that can take data, and based on how well it has been trained, will classify the text as 
positive or negative overall. It will  also provide visualizations which can be downloaded and inspected with some functionality

"""

import json
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO
from PIL import Image
import os

# Load AFINN111 list
afinn = None
with open('afinn111.json', 'r') as f:
    afinn = json.load(f)

def analyze_sentiment(text_widget, labels):
    """
    Analyze sentiment based on AFINN111 word list.

    Parameters:
    - text_widget (tk.Text): The Text widget containing input text.
    - labels (dict): Dictionary containing labels for displaying results.
    """
    text = text_widget.get("1.0", tk.END).strip()
    words = text.split()
    positive_words = []
    negative_words = []
    sentence_scores = []

    total_score = 0

    for index, word in enumerate(words):
        word = word.lower()
        if word in afinn:
            score = afinn[word]
            total_score += score
            if score > 0:
                positive_words.append(f'{word}: {score} ({index})')
            elif score < 0:
                negative_words.append(f'{word}: {score} ({index})')

            sentence_scores.append(score)

    # Update labels with sentiment analysis results
    labels["score"].config(text=f'Score: {total_score}')
    labels["comparative"].config(text=f'Comparative: {total_score / len(words):.2f}')
    labels["positive"].config(text=' '+ 'Positive Words:\n'+ ', '.join(positive_words), wraplength=700)
    labels["negative"].config(text='Negative Words:\n' + ', '.join(negative_words), wraplength=700)

    # Plotting charts in the same window
    plot_charts(sentence_scores, positive_words, negative_words, labels)

def plot_charts(sentence_scores, positive_words, negative_words, labels):
    """
    Plot sentiment charts and display them in the same window.

    Parameters:
    - sentence_scores (list): List of sentiment scores for each word.
    - positive_words (list): List of positive words with their scores and indices.
    - negative_words (list): List of negative words with their scores and indices.
    - labels (dict): Dictionary containing labels for displaying results.
    """
    # Combine positive and negative words and their scores
    all_words = []
    all_scores = []

    for word_entry in positive_words + negative_words:
        word, score_index = word_entry.split(":")
        word_index = int(score_index.split("(")[1].split(")")[0])
        all_words.append((word, word_index))
        all_scores.append(float(afinn[word]))

    # Sort words and scores based on their index in the sentence
    sorted_words_scores = sorted(zip(all_words, all_scores), key=lambda x: x[0][1])

    sorted_words, sorted_scores = zip(*sorted_words_scores)

    # Bar chart for words and their scores
    bar_colors = ['green' if score >= 0 else 'red' for score in sorted_scores]
    plt.bar(range(len(sorted_scores)), sorted_scores, color=bar_colors, width=0.8)
    plt.title('Sentiment for Each Word')
    plt.ylabel('Sentiment Score')
    plt.xlabel('Word Index')
    plt.xticks(range(len(sorted_words)), [word[0] for word in sorted_words], rotation=45, ha="right")

    # Pie chart
    num_negative = len([score for score in sentence_scores if score < 0])
    num_positive = len([score for score in sentence_scores if score >= 0])
    plt.figure()
    plt.pie([num_positive, num_negative], labels=['Positive', 'Negative'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    plt.title('Sentiment Distribution')

    # Line graph
    plt.figure()
    plt.plot(range(len(sentence_scores)), sentence_scores, marker='o', linestyle='-', color='blue')
    plt.title('Sentiment Along Sentence')
    plt.ylabel('Sentiment Score')
    plt.xlabel('Word Index')

    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to create a Tkinter GUI for sentiment analysis.
    """
    root = tk.Tk()
    root.title("Sentiment Analysis")

    # Center the window on the screen
    window_width = 800  # Set your desired window width
    window_height = 600  # Set your desired window height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    style = ttk.Style()

    # Set a consistent background color
    root.configure(bg="#333")
    style.configure("TFrame", background="#333")
    style.configure("TLabel", background="#333", foreground="#fff", font=("Helvetica", 12))
    style.configure("TButton", background="#008000", foreground="#333", font=("Helvetica", 12, "bold"), padding=10)

    frame = ttk.Frame(root, padding="10", style="TFrame")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    label = ttk.Label(frame, text="Enter text for sentiment analysis:", style="TLabel", justify='left')
    label.grid(column=0, row=0, columnspan=2, pady=10, sticky=tk.W)

    # Use a Text widget for multiline input
    text_widget = tk.Text(frame, wrap=tk.WORD, width=80, height=10, font=("Arial", 12), padx=5, pady=5)
    text_widget.grid(column=0, row=1, columnspan=2, pady=5, sticky=tk.W)

    analyze_button = ttk.Button(frame, text="Analyze Sentiment", command=lambda: analyze_sentiment(text_widget, labels), style="TButton")
    analyze_button.grid(column=0, row=2, columnspan=2, pady=10, sticky=tk.W)

    labels = {
        "score": ttk.Label(frame, text="Score: ", style="TLabel", justify="left"),
        "comparative": ttk.Label(frame, text="Comparative: ", style="TLabel", justify="left"),
        "positive": ttk.Label(frame, text="Positive Words:\n"+' ', style="TLabel", wraplength=600, justify="left"),
        "negative": ttk.Label(frame, text="Negative Words:\n", style="TLabel", wraplength=600, justify="left"),
    }

    for label_name, label_widget in labels.items():
        label_widget.grid(column=0, row=4 + list(labels.keys()).index(label_name), columnspan=2, pady=(10, 0), sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    main()