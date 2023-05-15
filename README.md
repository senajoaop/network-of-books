# Network of Books - Character Interaction Analysis

This repository contains a Python script that performs Natural Language Processing (NLP) analysis on an input book, characterizing the network of all characters based on their interactions. The example provided focuses on the Neapolitan Novels, also known as the Neapolitan Quartet, which is a four-part series of fiction written by the pseudonymous Italian author Elena Ferrante.

![Network Graph](data/net.png)
![Community Aggregation Graph](data/net_com.png)

## Dependencies

To run the analysis script, make sure you have the required dependencies installed. You can install them by running the following command:

`pip install -r requirements.txt`

The dependencies are listed in the `requirements.txt` file.

## Usage

1. Clone the repository: `git clone https://github.com/senajoaop/network-of-books.git`
2. Navigate to the project directory: `cd network-of-books`
3. Place your input book(s) in the `data` folder. The book(s) should be in `.txt` or `.pdf` format. If a PDF file is provided, it will be automatically converted to a text file.
4. Run the analysis script: `python BookNetwork.py`
5. The resulting character network graphs will be saved as HTML files in the `data` folder.
   - Individual Result: `network_result.html`
   - Community Aggregation Result: `network_com_result.html`

## Repository Structure

The repository has the following structure:

- `BookNetwork.py`: The Python script that performs the NLP analysis and generates the character network graphs.
- `data/`: A folder to store input book(s) and generated output files, including the network graphs and images.
- `net.png`: Image file containing the individual character interaction network graph.
- `net_com.png`: Image file containing the character interaction network graph with community aggregation.
- `network_result.html`: The resulting character interaction network graph.
- `network_com_result.html`: The resulting character interaction network graph with community aggregation.
- `requirements.txt`: A file listing all the required dependencies.
- `README.md`: The documentation file you are currently reading.

## Contributing

Contributions to this repository are welcome! If you have any improvements, suggestions, or bug fixes, please feel free to contribute by following these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your commit message"`
4. Push the branch to your forked repository: `git push origin feature/your-feature-name`
5. Open a pull request to the main repository.

Please ensure that your contributions align with the existing coding style and best practices.
