#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:28:43 2023

@author: samstroup
"""

# Import the necessary modules from the Opentrons package
# protocol_api for defining and executing protocols
# types for specifying locations in a protocol
from opentrons import protocol_api, types

# Define the metadata for the protocol
metadata = {
    'apiLevel': '2.11',  # The API version that the protocol is compatible with
    'protocolName': 'Hampton 24 Well Crystal Growth',  # The name of the protocol
    'description': '''A protocol for growing CJ crystals with custom 
     labware as provided by the OpenTrons team. This file name is 
     hamptonresearch_24_wellplate_24x500ul.json''',  # A description of the protocol
    'author': 'Jacob DeRoo'  # The author of the protocol
}

# Define the main function that will be run by the Opentrons robot
def run(protocol: protocol_api.ProtocolContext):
    # Load the labware
    # Load a 50ml conical tube rack in slot 2
    reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2)  
    # Load a 24 well plate in slot 3
    plate = protocol.load_labware('hamptonresearch_24_wellplate_24x500ul', 3)  
    # Load a 10ul tip rack in slot 1
    tips_1ul = protocol.load_labware('geb_96_tiprack_10ul', 1)  
    # Load a 200ul tip rack in slot 4
    tips_300ul = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)  
    
    # Define the pipettes
    # Load a p300 single-channel pipette on the right mount
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips_300ul])  
    # Load a p10 single-channel pipette on the left mount
    p10 = protocol.load_instrument('p10_single', 'left', tip_racks=[tips_1ul])  

    # Define the source wells in the reservoir
    # Source well A1 in the reservoir
    source_well_A1 = reservoir['A1']  
    # Source well A2 in the reservoir
    source_well_A2 = reservoir['A2']  
    # Source well A3 in the reservoir
    source_well_A3 = reservoir['A3']  

    # List of volumes to dispense in each well from reservoir A2
    volumes_reservoir_A2 = [9.0, 8.65, 8.30, 7.96, 7.61, 7.26, 6.91, 6.57, 6.22, 5.87, 5.52, 5.17, 4.83, 4.48, 4.13, 3.78, 3.43, 3.09, 2.74, 2.39, 2.04, 1.70, 1.35, 1.0]
    
    # List of volumes to dispense in each well from reservoir A3
    volumes_reservoir_A3 = [1.0, 1.35, 1.70, 2.04, 2.39, 2.74, 3.09, 3.43, 3.78, 4.13, 4.48, 4.83, 5.17, 5.52, 5.87, 6.22, 6.57, 6.91, 7.26, 7.61, 7.96, 8.30, 8.65, 9.0]

    # Offset in the x-direction (adjust this value as needed)
    x_offset = 4

    # Pick up a new tip with the p300 pipette
    p300.pick_up_tip()

    # Iterate through all the wells in the plate
    for well in plate.wells():
        # Aspirate 200uL from source well A1
        p300.aspirate(200, source_well_A1)  
        # Move to the well, offset in the x-direction
        p300.move_to(well.top().move(types.Point(x=x_offset, y=0, z=0)))  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Dispense 200uL into the well
        p300.dispense(200)  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Blow out to ensure no liquid remains in the pipette tip
        p300.blow_out()  

        # Pause for 1 second
        protocol.delay(seconds=1)  

    # Drop the used tip
    p300.drop_tip()  

    # Pick up a new tip with the p10 pipette
    p10.pick_up_tip()  

    # Dispense volumes from reservoir A2 into each well
    for well, volume_A2 in zip(plate.wells(), volumes_reservoir_A2):
        # Aspirate the specified volume from source well A2
        p10.aspirate(volume_A2, source_well_A2)  
        # Move to the well
        p10.move_to(well.top())  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Dispense the volume into the well
        p10.dispense(volume_A2)  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Blow out to ensure no liquid remains in the pipette tip
        p10.blow_out()  

        # Touch the tip to the well with a specified offset
        p10.touch_tip(radius=0.1, v_offset=-1.3)  

        # Pause for 1 second
        protocol.delay(seconds=1)  

    # Drop the used tip
    p10.drop_tip()  

    # Pick up a new tip with the p10 pipette
    p10.pick_up_tip()  

    # Dispense volumes from reservoir A3 into each well
    for well, volume_A3 in zip(plate.wells(), volumes_reservoir_A3):
        # Aspirate the specified volume from source well A3
        p10.aspirate(volume_A3, source_well_A3)  
        # Move to the well
        p10.move_to(well.top())  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Dispense the volume into the well
        p10.dispense(volume_A3)  

        # Pause for 0.5 seconds
        protocol.delay(seconds=0.5)  

        # Blow out
