class CardassianControlBajor:
    def __init__(self):
        self.occupation_status = "active"
        self.resistance = []
        self.power_holds = ["military occupation", "propaganda", "resource exploitation"]

    def enforce_control(self):
        print("Maintaining control over Bajor...")
        if self.occupation_status == "active":
            self.deploy_forces()
            self.suppress_resistance()
            self.extract_resources()

    def deploy_forces(self):
        print("Deploying Cardassian forces to key locations on Bajor.")

    def suppress_resistance(self):
        print("The resistance of Bajor will not be tolerated. Any act of defiance will be met with force.")
        # Simulating the capture of a resistance member
        self.resistance.append("captured member")

    def extract_resources(self):
        print("All Bajoran resources are now property of the Cardassian Union.")

    def propaganda(self):
        messages = [
            "Cardassia brings order and progress to Bajor.",
            "Cooperation with Cardassian authorities is in the best interest of all Bajorans."
        ]
        for message in messages:
            print(f"Broadcasting message: {message}")

    def attention_bajoran_workers(self):
        print("Attention Bajoran workers:")
        user_message = input("Enter your message: ")
        print(user_message)

    def status_update(self):
        if self.resistance:
            print("Resistance detected. Increasing security measures.")
        else:
            print("Bajor is fully under Cardassian control. No resistance detected.")

    # def end_occupation(self):
    #     print("Ending the occupation of Bajor.")
    #     self.occupation_status = "ended"
    #     print("Bajor is now free from Cardassian control.")
