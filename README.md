# Bar de Recherche

## Introduction

"Bar de Recherche" is a web application that allows users to search for bars near one or more addresses. The app is designed to be simple and intuitive, making it easy for users to find bars in specific locations with just a few clicks.

## Features

- **Multi-Address Search:** Users can input up to 5 different addresses to search for bars near those locations.
- **Interactive Map:** The app generates a map that displays the location of bars near the entered addresses.
- **Bar List:** A detailed list of bars, including their names and addresses, is provided alongside the map.

## How It Works

1. **Enter Addresses:**
   - The user can specify how many addresses they want to enter (between 1 and 5).
   - After specifying the number, input fields will be generated for each address.

2. **Generate Map:**
   - Once the addresses are entered, the user can click the "Générer la carte" button to create a map showing bars near the specified locations.
   - The map is displayed on the right side of the screen.

3. **View Bar List:**
   - Below the map, a list of bars near the entered addresses is shown, including the bar's name and address.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, jQuery
- **Backend:** Python (Flask)
- **Mapping API:** Integrated with a mapping service to generate maps and locate bars.

## How to Run the App

1. **Install Dependencies:**
   - Make sure you have Python and Flask installed on your machine.
   - Install the necessary Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the Application:**
   - Start the Flask server:
     ```bash
     python app.py
     ```
   - Open a web browser and navigate to `http://127.0.0.1:5000` to use the app.

3. **Use the Application:**
   - Enter one or more addresses, generate the map, and explore the bars near those locations.

## Future Enhancements

- **Filter Bars:** Add filtering options to narrow down the list of bars based on user preferences (e.g., rating, price range).
- **Favorite Bars:** Allow users to save their favorite bars for future reference.
- **Mobile Optimization:** Improve the user interface for better performance on mobile devices.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
