import datetime
import json
import os
from typing import List, Dict, Optional

class FitnessActivity:
    def __init__(self, activity_type: str, duration: float, calories: float, 
                 date: str = None, distance: float = None, notes: str = None):
        self.activity_type = activity_type
        self.duration = duration  # in minutes
        self.calories = calories  # calories burned
        self.distance = distance  # in kilometers (optional)
        self.notes = notes  # additional notes
        
        # Set date to current date if not provided
        self.date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self) -> Dict:
        """Convert activity to dictionary for storage"""
        return {
            'activity_type': self.activity_type,
            'duration': self.duration,
            'calories': self.calories,
            'distance': self.distance,
            'date': self.date,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FitnessActivity':
        """Create activity from dictionary"""
        return cls(
            activity_type=data['activity_type'],
            duration=data['duration'],
            calories=data['calories'],
            distance=data.get('distance'),
            date=data.get('date'),
            notes=data.get('notes')
        )

class FitnessTracker:
    def __init__(self, data_file: str = 'fitness_data.json'):
        self.data_file = data_file
        self.activities: List[FitnessActivity] = []
        self.load_data()
    
    def add_activity(self, activity: FitnessActivity) -> None:
        """Add a new activity to the tracker"""
        self.activities.append(activity)
        self.save_data()
    
    def delete_activity(self, index: int) -> bool:
        """Delete an activity by index"""
        if 0 <= index < len(self.activities):
            del self.activities[index]
            self.save_data()
            return True
        return False
    
    def get_activities_by_date(self, date: str) -> List[FitnessActivity]:
        """Get all activities for a specific date"""
        return [activity for activity in self.activities if activity.date == date]
    
    def get_activities_by_type(self, activity_type: str) -> List[FitnessActivity]:
        """Get all activities of a specific type"""
        return [activity for activity in self.activities 
                if activity.activity_type.lower() == activity_type.lower()]
    
    def get_total_calories(self) -> float:
        """Get total calories burned across all activities"""
        return sum(activity.calories for activity in self.activities)
    
    def get_total_duration(self) -> float:
        """Get total duration across all activities (in minutes)"""
        return sum(activity.duration for activity in self.activities)
    
    def get_weekly_summary(self, weeks_ago: int = 0) -> Dict[str, float]:
        """Get weekly summary of calories and duration"""
        end_date = datetime.datetime.now() - datetime.timedelta(weeks=weeks_ago)
        start_date = end_date - datetime.timedelta(days=7)
        
        weekly_activities = [
            activity for activity in self.activities
            if start_date <= datetime.datetime.strptime(activity.date, "%Y-%m-%d") <= end_date
        ]
        
        total_calories = sum(activity.calories for activity in weekly_activities)
        total_duration = sum(activity.duration for activity in weekly_activities)
        
        return {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'total_calories': total_calories,
            'total_duration': total_duration,
            'activity_count': len(weekly_activities)
        }
    
    def save_data(self) -> None:
        """Save activities to file"""
        with open(self.data_file, 'w') as f:
            json.dump([activity.to_dict() for activity in self.activities], f)
    
    def load_data(self) -> None:
        """Load activities from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.activities = [FitnessActivity.from_dict(item) for item in data]
    
    def display_all_activities(self) -> None:
        """Display all activities in a readable format"""
        print("\nAll Fitness Activities:")
        print("-" * 50)
        for i, activity in enumerate(self.activities, 1):
            print(f"{i}. {activity.date} - {activity.activity_type}")
            print(f"   Duration: {activity.duration} min | Calories: {activity.calories}")
            if activity.distance:
                print(f"   Distance: {activity.distance} km")
            if activity.notes:
                print(f"   Notes: {activity.notes}")
            print("-" * 50)

def main():
    tracker = FitnessTracker()
    
    while True:
        print("\nFitness Tracker Menu:")
        print("1. Add new activity")
        print("2. View all activities")
        print("3. View activities by date")
        print("4. View activities by type")
        print("5. View weekly summary")
        print("6. Delete an activity")
        print("7. View total statistics")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            print("\nAdd New Activity")
            activity_type = input("Activity type (e.g., Running, Swimming): ")
            duration = float(input("Duration (minutes): "))
            calories = float(input("Calories burned: "))
            distance = input("Distance (km, optional - press enter to skip): ")
            notes = input("Notes (optional - press enter to skip): ")
            
            activity = FitnessActivity(
                activity_type=activity_type,
                duration=duration,
                calories=calories,
                distance=float(distance) if distance else None,
                notes=notes if notes else None
            )
            
            tracker.add_activity(activity)
            print("Activity added successfully!")
        
        elif choice == '2':
            tracker.display_all_activities()
        
        elif choice == '3':
            date = input("Enter date (YYYY-MM-DD): ")
            activities = tracker.get_activities_by_date(date)
            if activities:
                print(f"\nActivities on {date}:")
                for i, activity in enumerate(activities, 1):
                    print(f"{i}. {activity.activity_type} - {activity.duration} min, {activity.calories} cal")
            else:
                print("No activities found for this date.")
        
        elif choice == '4':
            activity_type = input("Enter activity type: ")
            activities = tracker.get_activities_by_type(activity_type)
            if activities:
                print(f"\nAll {activity_type} activities:")
                for i, activity in enumerate(activities, 1):
                    print(f"{i}. {activity.date} - {activity.duration} min, {activity.calories} cal")
            else:
                print(f"No {activity_type} activities found.")
        
        elif choice == '5':
            weeks_ago = int(input("Enter how many weeks ago (0 for current week): "))
            summary = tracker.get_weekly_summary(weeks_ago)
            print(f"\nWeekly Summary ({summary['start_date']} to {summary['end_date']}):")
            print(f"Total Activities: {summary['activity_count']}")
            print(f"Total Duration: {summary['total_duration']} minutes")
            print(f"Total Calories Burned: {summary['total_calories']}")
        
        elif choice == '6':
            tracker.display_all_activities()
            if tracker.activities:
                index = int(input("Enter activity number to delete: ")) - 1
                if tracker.delete_activity(index):
                    print("Activity deleted successfully!")
                else:
                    print("Invalid activity number.")
        
        elif choice == '7':
            print("\nTotal Statistics:")
            print(f"Total Activities: {len(tracker.activities)}")
            print(f"Total Duration: {tracker.get_total_duration()} minutes")
            print(f"Total Calories Burned: {tracker.get_total_calories()}")
        
        elif choice == '8':
            print("Exiting Fitness Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()