import os
import subprocess

# Output directories
os.makedirs("public/images", exist_ok=True)
os.makedirs("scratch", exist_ok=True)

# -------------------------------------------------------------
# ICON EMBLEM DEFINITIONS (Vector paths for the speed courier)
# -------------------------------------------------------------
# SQUIRCLE EMBLEM: x=100, y=100, size=220x220
# Inside: Rider in motion, front wheel, back wheel, delivery box, speed lines

def get_emblem_svg(x_offset=0, y_offset=0, scale=1.0):
    return f"""
    <g transform="translate({x_offset}, {y_offset}) scale({scale})">
      <!-- Outer Glow / Soft Rim -->
      <rect x="20" y="20" width="220" height="220" rx="55" fill="url(#emeraldGrad)" />
      
      <!-- Inner subtle geometric border -->
      <rect x="24" y="24" width="212" height="212" rx="51" fill="none" stroke="#6EE7B7" stroke-width="2" opacity="0.4" />
      
      <!-- Speed Motion Wind Trails Behind Bike -->
      <path d="M 45 105 L 85 105" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.4" />
      <path d="M 35 130 L 75 130" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7" />
      <path d="M 50 155 L 90 155" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.4" />

      <!-- THE MOTORCYCLE & COURIER SILHOUETTE (Clean Vector Geometry) -->
      <g fill="#064E3B">
        <!-- Rear Wheel -->
        <circle cx="85" cy="165" r="24" fill="#0F172A" stroke="#FFFFFF" stroke-width="6"/>
        <circle cx="85" cy="165" r="9" fill="#10B981" />
        
        <!-- Front Wheel -->
        <circle cx="178" cy="165" r="24" fill="#0F172A" stroke="#FFFFFF" stroke-width="6"/>
        <circle cx="178" cy="165" r="9" fill="#10B981" />

        <!-- Motorcycle Frame & Engine Core -->
        <path d="M 85 165 L 118 142 L 148 142 L 178 165 L 158 135 L 125 135 Z" fill="#FFFFFF" />

        <!-- Front Fork & Handlebars -->
        <path d="M 178 165 L 152 112 L 140 114" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <!-- Aerodynamic Windshield -->
        <path d="M 152 112 L 165 98 L 155 96 Z" fill="#6EE7B7" />

        <!-- Insulated Delivery Box on Rear Rack -->
        <rect x="68" y="108" width="36" height="34" rx="6" fill="#FFFFFF" stroke="#0F172A" stroke-width="3"/>
        <path d="M 74 125 L 98 125" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>

        <!-- Rider Body (Forward Leaning Aero Posture) -->
        <!-- Torso -->
        <path d="M 98 126 C 105 110, 118 105, 136 114 L 148 124 L 138 135 L 118 132 Z" fill="#0F172A"/>
        <!-- Rider Arm Reaching Handlebars -->
        <path d="M 125 116 L 145 120 L 150 114" stroke="#0F172A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        
        <!-- Rider Helmet with Visor -->
        <circle cx="132" cy="94" r="16" fill="#0F172A" stroke="#FFFFFF" stroke-width="2.5"/>
        <!-- Emerald Visor Cut -->
        <path d="M 136 88 C 144 90, 146 98, 144 102 L 136 100 Z" fill="#34D399" />
      </g>
    </g>
    """

print("Generator script template ready")
