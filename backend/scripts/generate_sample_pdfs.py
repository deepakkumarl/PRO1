import os
from pathlib import Path

def create_pdfs():
    """Generates 4 detailed synthetic BMW Service PDF Manuals using ReportLab."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        print("Reportlab not installed. Installing or fallback script required.")
        return

    output_dir = Path(__file__).resolve().parent.parent / "data" / "documents"
    output_dir.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#006699'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#222222'),
        spaceAfter=8
    )

    warning_style = ParagraphStyle(
        'Warning',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#CC0000'),
        backColor=colors.HexColor('#FFEEEE'),
        borderColor=colors.HexColor('#CC0000'),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=10
    )

    # 1. BMW EV Battery Service Manual
    doc1_path = output_dir / "bmw_ev_battery_service.pdf"
    doc1 = SimpleDocTemplate(str(doc1_path), pagesize=letter)
    story1 = [
        Paragraph("BMW Technical Service Information: EV High-Voltage Battery Module & Thermal Management", title_style),
        Paragraph("Document ID: BMW-TSB-2026-EV01 | Section: Electric Drivetrain & Battery System", body_style),
        Spacer(1, 10),
        
        Paragraph("Page 1: Battery Pack Architecture & Overview", heading_style),
        Paragraph("The BMW Electric Vehicle (EV) high-voltage battery unit consists of modular lithium-ion battery cell modules connected in series/parallel configurations. The battery system is monitored by the Battery Management Electronics (SME) control unit and Cell Supervision Circuits (CSC).", body_style),
        Paragraph("Operating Parameters: Nominal Voltage: 350V - 800V depending on vehicle architecture. Maximum cell operating temperature threshold: 45°C. Critical overheat alert threshold: 55°C.", body_style),
        
        Spacer(1, 15),
        Paragraph("Page 2: Repeated EV Battery Overheating Diagnostics", heading_style),
        Paragraph("<b>Symptom:</b> Vehicle displays high-voltage battery over-temperature warning on Instrument Cluster / ISTA fault code 21F004 (Battery Cell Temperature Exceeded Threshold).", body_style),
        Paragraph("<b>Required Inspection Procedure for Battery Overheating:</b>", body_style),
        Paragraph("1. Inspect the high-voltage coolant loop circulation pump (M50 auxiliary pump) for proper operating duty cycle and pressure output.", body_style),
        Paragraph("2. Check coolant fluid level in the secondary low-temperature cooling circuit (BMW HT-12 approved coolant solution). Low coolant level causes air locks in the battery heat exchanger plate.", body_style),
        Paragraph("3. Inspect the coolant switching valve (3-way solenoid valve) for mechanical stickiness or diagnostic trouble code 21F08A.", body_style),
        Paragraph("4. Check the battery thermal interface material (TIM / gap filler) under the lower battery tray for voiding, thermal degradation, or physical separation.", body_style),
        Paragraph("5. Perform cell balancing readout via ISTA service functions to identify individual module temperature sensor deviations. If one CSC reports >10°C higher than adjacent modules, check module connector contacts.", body_style),
        
        Spacer(1, 15),
        Paragraph("Page 3: Battery Module Replacement & Torque Specifications", heading_style),
        Paragraph("When replacing an individual high-voltage battery module, adhere strictly to the following torque specifications:", body_style),
        Paragraph("• Battery Module Busbar M6 Fasteners: 9.5 Nm ± 0.5 Nm.", body_style),
        Paragraph("• Battery Enclosure Frame M8 Bolts: 22 Nm (use new micro-encapsulated bolts).", body_style),
        Paragraph("• Coolant Line Hose Clamps to Heat Exchanger: Hand-tighten until torque click indicator engages (2.2 Nm).", body_style),
    ]
    doc1.build(story1)
    print(f"Created {doc1_path.name}")

    # 2. BMW Cooling System Service Manual
    doc2_path = output_dir / "bmw_cooling_system.pdf"
    doc2 = SimpleDocTemplate(str(doc2_path), pagesize=letter)
    story2 = [
        Paragraph("BMW Technical Service Manual: Electric & Auxiliary Cooling Systems", title_style),
        Paragraph("Document ID: BMW-TSB-2026-COOL02 | Section: Thermal Management & HVAC", body_style),
        Spacer(1, 10),
        
        Paragraph("Page 1: Cooling Loop Architecture", heading_style),
        Paragraph("BMW vehicles feature dual thermal management loops: High-Temperature (HT) circuit for power electronics / motor cooling, and Low-Temperature (LT) circuit for battery module cooling and cabin HVAC heat exchange.", body_style),
        
        Spacer(1, 15),
        Paragraph("Page 2: Cooling System Troubleshooting & Diagnostics", heading_style),
        Paragraph("<b>Symptoms of Cooling System Malfunction:</b> High electric motor temperature fault, degraded cabin A/C battery chilling performance, or noisy electric water pump operation.", body_style),
        Paragraph("<b>Inspection Steps:</b>", body_style),
        Paragraph("1. Check for physical leaks around the electric water pump casing and coolant hoses.", body_style),
        Paragraph("2. Verify radiator shuttle valve / electric radiator flap actuators move freely without binding.", body_style),
        Paragraph("3. Run the automated vacuum filling and bleeding procedure using BMW Special Tool 17 0 020. Never refill coolant manually without vacuum evacuation as air pockets will cause localized thermal runaway.", body_style),
        Paragraph("4. Verify temperature sensor accuracy: Compare readings between NTC Sensor 1 (Inlet) and NTC Sensor 2 (Outlet). Max allowed variance when cold is 2.0°C.", body_style),
    ]
    doc2.build(story2)
    print(f"Created {doc2_path.name}")

    # 3. BMW High Voltage Safety Service Manual
    doc3_path = output_dir / "bmw_high_voltage_safety.pdf"
    doc3 = SimpleDocTemplate(str(doc3_path), pagesize=letter)
    story3 = [
        Paragraph("BMW High-Voltage Safety Requirements & De-Energization Standard Operating Procedure", title_style),
        Paragraph("Document ID: BMW-SOP-2026-HVS03 | Section: Safety Standards & De-Energization", body_style),
        Spacer(1, 10),
        
        Paragraph("Page 1: High-Voltage Safety Warning & PPE Requirements", heading_style),
        Paragraph("<b>CRITICAL SAFETY WARNING:</b> High-voltage systems operate at potentials exceeding 600V DC. Touch contact with live components can cause fatal electric shock or severe burns.", warning_style),
        Paragraph("<b>Mandatory Personal Protective Equipment (PPE):</b>", body_style),
        Paragraph("• Class 0 IEC 60903 insulated safety gloves rated for minimum 1000V AC / 1500V DC (inspected and pressure-tested before every use).", body_style),
        Paragraph("• Outer leather protector gloves to prevent mechanical damage to insulated rubber gloves.", body_style),
        Paragraph("• Arc flash face shield (ANSI Z87.1 / ASTM F2178 compliant).", body_style),
        Paragraph("• Insulated safety footwear and non-conductive cotton working apparel.", body_style),

        Spacer(1, 15),
        Paragraph("Page 2: High-Voltage System De-Energization & Lockout Procedure", heading_style),
        Paragraph("<b>Step-by-Step HV De-Energization Protocol:</b>", body_style),
        Paragraph("1. Turn off ignition switch and move key fob outside 5-meter radius.", body_style),
        Paragraph("2. Disconnect 12V auxiliary ground battery cable to prevent automatic contactor closure.", body_style),
        Paragraph("3. Remove High-Voltage Service Disconnect Plug (HV Safety Connector) located in rear luggage compartment or under lower engine cover.", body_style),
        Paragraph("4. Attach padlocked Lockout/Tagout (LOTO) safety lock to the service disconnect housing.", body_style),
        Paragraph("5. Wait 5 minutes for internal high-voltage DC bus capacitors to discharge through internal discharge resistors.", body_style),
        Paragraph("6. Perform 3-Point Voltage-Free Verification Test using a CAT IV 1000V rated calibrated multimeter:", body_style),
        Paragraph("   a) Test meter against known live voltage source.", body_style),
        Paragraph("   b) Test between HV positive (+) terminal and chassis ground (must read < 5.0V DC).", body_style),
        Paragraph("   c) Test between HV negative (-) terminal and chassis ground (must read < 5.0V DC).", body_style),
        Paragraph("   d) Test between HV positive (+) and negative (-) terminals (must read < 5.0V DC).", body_style),
        Paragraph("   e) Re-verify meter calibration against known live voltage source.", body_style),
    ]
    doc3.build(story3)
    print(f"Created {doc3_path.name}")

    # 4. BMW Diagnostics Service Manual
    doc4_path = output_dir / "bmw_diagnostics.pdf"
    doc4 = SimpleDocTemplate(str(doc4_path), pagesize=letter)
    story4 = [
        Paragraph("BMW Diagnostics & ISTA Operation Guide", title_style),
        Paragraph("Document ID: BMW-TSB-2026-DIAG04 | Section: ISTA Diagnostics & Fault Memory", body_style),
        Spacer(1, 10),
        
        Paragraph("Page 1: ISTA System Overview", heading_style),
        Paragraph("Integrated Service Technical Application (ISTA) is the primary diagnostic system for BMW vehicles. ISTA provides guided troubleshooting, wiring diagrams, component locations, and test plans.", body_style),
        
        Spacer(1, 15),
        Paragraph("Page 2: Diagnostic Trouble Code (DTC) Analysis & Readout", heading_style),
        Paragraph("<b>Common Fault Codes:</b>", body_style),
        Paragraph("• <b>21F004:</b> High Voltage Battery Cell Temperature Exceeded Limit - Indicates cooling system fault or degraded thermal interface.", body_style),
        Paragraph("• <b>21F08A:</b> Battery Coolant Switching Valve Actuation Fault - Inspect electrical connector X14*1B.", body_style),
        Paragraph("• <b>10AA01:</b> Auxiliary Electric Water Pump Duty Cycle Out of Specification.", body_style),
        Paragraph("• <b>0020A1:</b> High-Voltage Safety Line Interrupted (HV Interlock Open Loop).", body_style),
        Paragraph("<b>Diagnostic Execution:</b> Connect ICOM A2/A3 interface to vehicle OBD port. Scan complete vehicle control unit tree. Execute ISTA Guided Troubleshooting Test Plan before clearing fault memory.", body_style),
    ]
    doc4.build(story4)
    print(f"Created {doc4_path.name}")

if __name__ == "__main__":
    create_pdfs()
