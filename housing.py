# store your content here at your database of choose so as to retrieve them during the nearby logic
class UnifiedDatabase:
    def __init__(self):
        # Connect (or create) the unified SQLite database file.
        conn = sqlite3.connect('unified_data.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS house_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,                  -- House name
            location TEXT,               -- House location
            price TEXT,                  -- House price
            available_space TEXT,        -- Available space information
            house_check_value TEXT,      -- Check value or verification status as text
            description TEXT,            -- House description
            verified_icon TEXT,
            agent_id TEXT,
            street TEXT,
            latitude REAL,
            longitude REAL,
            thumbnail TEXT,              -- Thumbnail image (first image)
            images TEXT,                 -- JSON serialized list of all image paths
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 2. Shortlets Table: For shortlet listings.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortlet_details(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,                  -- House name
            location TEXT,               -- House location
            price TEXT,                  -- House price
            shortlet_check_value TEXT,   -- Check value or verification status as text
            description TEXT,            -- House description
            agent_id TEXT,
            street TEXT,
            latitude REAL,
            longitude REAL,
            thumbnail TEXT,              -- Thumbnail image (first image)
            images TEXT,                 -- JSON serialized list of all image paths
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 3. Properties Table: For other property data.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS property_details(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,                  
            location TEXT,               
            price TEXT,                  
            property_check_value TEXT,   
            description TEXT, 
            agent_id TEXT,
            street TEXT,
            latitude REAL,
            longitude REAL,          
            thumbnail TEXT,              
            images TEXT,                 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

UnifiedDatabase()
    
class Main_page:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.vertical_alignment = CrossAxisAlignment.CENTER

        self.page.update()
        self.hold_view()

    def hold_view(self):
        self.page.controls.clear()
        self.hold_subview = ListView(
            controls=[],
            expand=True,
            auto_true=True
        )

        self.page.controls.append(self.hold_subview)
        self.page.update()
  
    def houses_nearby(self, e):
        """
        Determines the user's current coordinates, then uses reverse geocoding
        to extract both the broad location (e.g., city/state) and the street.
        """
        # Get user coordinates via IP-based geolocation.
        g = geocoder.ip('me')
        if not g.ok:
            Messagebox("Unable to determine location, check network.", self.page)
            return
        user_lat = g.latlng[0]
        user_lon = g.latlng[1]

        # Reverse geocode to get detailed address information.
        rev = geocoder.osm(
            [user_lat, user_lon],
            method='reverse',
            headers={'User-Agent': 'HouseAgentApp/1.0 ("Enter your email here")'}
        )
        # Try to extract a broad location (for example, city); fallback to state if needed.
        if rev.ok:
            user_location = rev.city if hasattr(rev, 'city') and rev.city else (rev.state if hasattr(rev, 'state') else "")
            user_street = rev.street if hasattr(rev, 'street') and rev.street else ""
        else:
            user_location = ""
            user_street = ""

        # Call the function that handles querying and UI reconstruction.
        self.suggest_houses(user_lat, user_lon, user_location, user_street)

    def suggest_houses(self, user_latitude, user_longitude, user_location, user_street):
        """
        Uses the reverse-geocoded broad location and street to query the database.
        For every candidate record, calculates distance; only those within the
        threshold are shown. Each result includes both textual address info and the
        computed distance.
        """
        # Clear previous subview content.
        self.hold_subview.controls.clear()

        # Create a back button to return to the main housing display.
        self.nearby_back_button = FloatingActionButton(
            icon=Icons.ARROW_BACK,
            tooltip="Back",
            on_click=lambda e: self.housing_display()
        )

        # Define a threshold distance (in kilometers).
        threshold = 10

        # Helper function to compute distance between two latitude/longitude points.
        def get_distance(lat1, lon1, lat2, lon2):
            from math import radians, cos, sin, sqrt, atan2
            R = 6371  # Earth's radius in km.
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        # Build wildcard strings for text-based matching.
        location_param = "%" + user_location + "%" if user_location else "%"
        street_param = "%" + user_street + "%" if user_street else "%"

        nearby_results = []

        # Open the database connection.
        conn = sqlite3.connect("unified_data.db")
        cursor = conn.cursor()

        # --- Query Houses ---
        cursor.execute("""
            SELECT id, title, location, price, images, latitude, longitude, street
            FROM house_details
            WHERE location LIKE ? AND street LIKE ?
        """, (location_param, street_param))
        houses = cursor.fetchall()

        for rec in houses:
            rec_id, title, location, price, images_json, lat, lon, street = rec
            if lat is None or lon is None:
                continue
            distance = get_distance(user_latitude, user_longitude, lat, lon)
            if distance <= threshold:
                try:
                    images = json.loads(images_json)
                except Exception:
                    images = []
                img_src = images[0] if images else ""
                house_container = Container(
                    content=Row(
                        controls=[
                            Image(src=img_src, width=200, height=150, border_radius=10),
                            Column(
                                controls=[
                                    Text(f"{title}", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_MEDIUM),
                                    Text(f"Location: {location}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Price: {price}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Street: {street}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"{distance:.1f} km away", style=TextThemeStyle.BODY_SMALL),
                                ],
                                spacing=5
                            )
                        ]
                    ),
                    bgcolor=Colors.LIGHT_GREEN_700,
                    alignment=alignment.center,
                    padding=10,
                    margin=10,
                    border_radius=10,
                    on_click=lambda e, data=rec: self.show_house_details(data)
                )
                nearby_results.append(house_container)

        # --- Query Shortlets ---
        cursor.execute("""
            SELECT id, title, location, price, images, latitude, longitude, street
            FROM shortlet_details
            WHERE location LIKE ? AND street LIKE ?
        """, (location_param, street_param))
        shotlets = cursor.fetchall()

        for rec in shotlets:
            rec_id, title, location, price, images_json, lat, lon, street = rec
            if lat is None or lon is None:
                continue
            distance = get_distance(user_latitude, user_longitude, lat, lon)
            if distance <= threshold:
                try:
                    images = json.loads(images_json)
                except Exception:
                    images = []
                img_src = images[0] if images else ""
                shotlet_container = Container(
                    content=Row(
                        controls=[
                            Image(src=img_src, width=200, height=150, border_radius=10),
                            Column(
                                controls=[
                                    Text(f"{title}", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_MEDIUM),
                                    Text(f"Location: {location}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Price: {price}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Street: {street}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"{distance:.1f} km away", style=TextThemeStyle.BODY_SMALL),
                                ],
                                spacing=5
                            )
                        ]
                    ),
                    bgcolor=Colors.LIGHT_GREEN_700,
                    alignment=alignment.center,
                    padding=10,
                    margin=10,
                    border_radius=10,
                    on_click=lambda e, data=rec: self.show_shortlet_details(data)
                )
                nearby_results.append(shotlet_container)

        # --- Query Properties ---
        cursor.execute("""
            SELECT id, title, location, price, images, latitude, longitude, street
            FROM property_details
            WHERE location LIKE ? AND street LIKE ?
        """, (location_param, street_param))
        properties = cursor.fetchall()

        for rec in properties:
            rec_id, title, location, price, images_json, lat, lon, street = rec
            if lat is None or lon is None:
                continue
            distance = get_distance(user_latitude, user_longitude, lat, lon)
            if distance <= threshold:
                try:
                    images = json.loads(images_json)
                except Exception:
                    images = []
                img_src = images[0] if images else ""
                property_container = Container(
                    content=Row(
                        controls=[
                            Image(src=img_src, width=200, height=150, border_radius=10),
                            Column(
                                controls=[
                                    Text(f"{title}", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_MEDIUM),
                                    Text(f"Location: {location}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Price: {price}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"Street: {street}", style=TextThemeStyle.BODY_SMALL),
                                    Text(f"{distance:.1f} km away", style=TextThemeStyle.BODY_SMALL),
                                ],
                                spacing=5
                            )
                        ]
                    ),
                    bgcolor=Colors.LIGHT_GREEN_700,
                    alignment=alignment.center,
                    padding=10,
                    margin=10,
                    border_radius=10,
                    on_click=lambda e, data=rec: self.show_property_details(data)
                )
                nearby_results.append(property_container)

        conn.close()

        # Build the UI: display a ListView of nearby results along with the back button.
        if nearby_results:
            self.nearby_list_view = Container(
                content=Column(
                    controls=[
                        self.nearby_back_button,
                        ListView(
                            controls=nearby_results,
                            auto_scroll=True,
                            expand=True,
                            divider_thickness=5,
                        )
                    ]
                ),
                expand=True,
            )
            self.hold_subview.controls.append(self.nearby_list_view)
        else:
            Messagebox("No nearby houses found", self.page)

        self.page.update()

if __name__ == "__main__":
    ft.app(target=Main_page)
