import requests
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.clock import mainthread
from dotenv import load_dotenv
import os
from app_state import state

load_dotenv(".env.development")  # Load environment variables from .env.
API_URL = os.getenv("API_URL")


class ReachSegmentTable(MDScreen):
    def __init__(self, **kwargs):
        super(ReachSegmentTable, self).__init__(**kwargs)

        # Initialize the data table (empty for now)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Reach Segment ID", dp(30)),
                ("Date", dp(30)),
                ("Status", dp(30)),
                ("Item Labels", dp(30)),
                ("Hand Labels", dp(30)),
                ("Polygons", dp(30)),
                ("Labeled By", dp(30)),
                ("Started On", dp(30)),
                ("Completed On", dp(30)),
                ("Generated", dp(30)),
            ],
            row_data=[],  # Initially empty; will be populated by GraphQL data
            sorted_on="Date",
            sorted_order="ASC",
            elevation=2,
        )

        # Fetch data from GraphQL and populate the table

        # Add the data table to the screen

    def on_parent(self, widget, parent):
        self.fetch_reach_segment_data()
        self.add_widget(self.data_tables)

    def fetch_reach_segment_data(self):
        """Fetches reach segment data from the GraphQL API and populates the table."""
        headers = {"Authorization": f"Token {state.token}"}
        with open("graphql/reach_segment_label_list.gql", "r") as file:
            query = file.read()
        variables = {
            "start": 0,
            "limit": 20,
            "status": 0,
            "itemIds": [],
            "stockwellIds": [],
            "userIds": [],
            "txnLimit": None,
        }

        json_data = {
            "operationName": "reachSegmentLabelList",
            "query": query,
            "variables": variables,
        }

        # Make the GraphQL request
        try:
            response = requests.post(API_URL, json=json_data, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Parse and populate the data table
            if "data" in data and data["data"].get("reachSegmentLabelList"):
                reach_segments = data["data"]["reachSegmentLabelList"]["reachSegments"]
                row_data = self.process_reach_segment_data(reach_segments)
                self.populate_table(row_data)
            else:
                toast("Failed to fetch data.")
        except requests.exceptions.HTTPError as http_err:
            toast(f"HTTP error occurred: {http_err}")
        except Exception as err:
            toast(f"An error occurred: {err}")

    def process_reach_segment_data(self, reach_segments):
        """Process the raw GraphQL response data to fit into the table."""
        row_data = []
        for segment in reach_segments:
            row = (
                str(segment["id"]),  # Reach Segment ID
                segment["date"],  # Date
                segment["labelStatus"]["status"],  # Status
                str(len(segment["labels"])),  # Item Labels (count)
                str(
                    sum(1 for label in segment["labels"] if label["type"] == "HAND")
                ),  # Hand Labels (count)
                str(
                    sum(len(label["polygons"]) for label in segment["labels"])
                ),  # Polygons (count)
                segment["labelStatus"]["labeledBy"]["username"],  # Labeled By
                segment["labelStatus"]["bornOn"],  # Started On
                segment["labelStatus"]["completeOn"],  # Completed On
                "Yes" if segment["labelStatus"]["wasGenerated"] else "No",  # Generated
            )
            row_data.append(row)
        return row_data

    @mainthread
    def populate_table(self, row_data):
        """Populate the data table with the fetched row data."""
        self.data_tables.row_data = row_data

    def on_row_press(self, instance_table, instance_row):
        """Called when a table row is clicked."""
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        """Called when the check box in the table row is checked."""
        print(instance_table, current_row)
