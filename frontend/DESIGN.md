---
name: Luxe Literary Collective
colors:
  surface: '#fff8f8'
  surface-dim: '#ecd4db'
  surface-bright: '#fff8f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff0f3'
  surface-container: '#ffe8ee'
  surface-container-high: '#fbe2e9'
  surface-container-highest: '#f5dce3'
  on-surface: '#25181d'
  on-surface-variant: '#574048'
  inverse-surface: '#3b2c31'
  inverse-on-surface: '#ffecf1'
  outline: '#8b7079'
  outline-variant: '#debec8'
  surface-tint: '#b4136d'
  primary: '#b10e6b'
  on-primary: '#ffffff'
  primary-container: '#d23284'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb0cd'
  secondary: '#a43073'
  on-secondary: '#ffffff'
  secondary-container: '#fc79bd'
  on-secondary-container: '#76014e'
  tertiary: '#783eb2'
  on-tertiary: '#ffffff'
  tertiary-container: '#9358cd'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9e4'
  primary-fixed-dim: '#ffb0cd'
  on-primary-fixed: '#3e0022'
  on-primary-fixed-variant: '#8c0053'
  secondary-fixed: '#ffd8e7'
  secondary-fixed-dim: '#ffafd3'
  on-secondary-fixed: '#3d0026'
  on-secondary-fixed-variant: '#85145a'
  tertiary-fixed: '#f0dbff'
  tertiary-fixed-dim: '#ddb8ff'
  on-tertiary-fixed: '#2c0051'
  on-tertiary-fixed-variant: '#62259b'
  background: '#fff8f8'
  on-background: '#25181d'
  surface-variant: '#f5dce3'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 56px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max-width: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  stack-xs: 8px
  stack-md: 24px
  stack-xl: 64px
---

## Brand & Style

This design system embodies a "Contemporary Ethereal" aesthetic—a fusion of high-end editorial luxury and cutting-edge AI fluidity. It is designed for a discerning audience that views reading not just as a hobby, but as a lifestyle of self-care and intellectual indulgence. 

The visual narrative is inspired by the frictionless elegance of premium tech and the inviting warmth of a boutique physical bookstore. Key characteristics include:
- **Sophisticated Softness:** Using a palette of blush whites and rose tones to create a calming, feminine environment.
- **Modern Clarity:** Borrowing the generous whitespace and high-clarity layouts of industry leaders like Apple and Airbnb.
- **Magical Precision:** Subtle "sparkle" motifs and gradient flows represent the AI's ability to discover the perfect story for the reader.
- **Glassmorphism:** Layers of frosted transparency suggest depth and a multi-dimensional browsing experience.

## Colors

The palette is anchored by **Soft Blush White (#FFF9FC)**, which provides a warmer, more premium alternative to pure white, reducing eye strain during long reading sessions. 

- **Rose Pink (#EC4899)** serves as the primary action color, used for high-intent interactions and branding.
- **Lavender Purple (#C084FC)** acts as the "AI signature" color, used for smart features and recommendations.
- **Gold (#FBBF24)** is reserved strictly for highlights, such as "Featured" tags, rare finds, or premium member statuses, evoking a sense of exclusivity.
- **The Gradient Flow** is a key brand asset, used in headers and hero sections to represent the transition from a blank page to a vivid imagination.

## Typography

This design system utilizes a high-contrast typographic pairing to evoke a "Modern Editorial" feel.

1.  **Playfair Display (Serif):** Used for large headings and display moments. Its classical proportions and delicate strokes signal authority and literary heritage.
2.  **Plus Jakarta Sans (Sans-Serif):** Chosen for its soft, rounded terminals that maintain a friendly and approachable tone for body copy and navigational elements.

**Usage Notes:**
- Keep tracking tight on large serifs to maintain a premium "magazine" look.
- Use wide tracking on labels to ensure legibility and a sense of luxury.
- Hero headings should always utilize the serif typeface to ground the AI-driven tech in traditional book culture.

## Layout & Spacing

The layout philosophy is **Generous and Fluid**. Content is never crowded; whitespace is treated as a design element itself to foster a feeling of calm.

- **Grid:** A 12-column grid for desktop with wide 24px gutters.
- **Margins:** Desktop margins are exceptionally wide (64px) to center the focus and mimic the margins of a printed book page.
- **The "Floating" Model:** Elements often ignore traditional containment. Cards should feel as though they are drifting over the background, utilizing a vertical rhythm based on 8px increments.
- **Mobile:** Transition to a 4-column grid with reduced margins (20px) to maximize screen real estate while maintaining a sense of "breathability."

## Elevation & Depth

Depth in this design system is achieved through "Ethereal Layering" rather than heavy, realistic shadows.

1.  **Soft Glassmorphism:** Primary containers (like Navigation bars and Modals) use a backdrop blur (20px-40px) with a semi-transparent white fill (opacity 70-80%). They should have a subtle 1px white inner stroke to define the edges.
2.  **Ambient Shadows:** For floating cards, use extremely diffused shadows. Avoid black; instead, use a shadow color derived from the primary rose hue (e.g., `rgba(236, 72, 153, 0.08)`) with a high blur radius (30px+).
3.  **The "Z-Axis" Narrative:**
    - **Level 0 (Base):** Soft Blush White background.
    - **Level 1 (Cards):** Solid white with ambient rose shadow.
    - **Level 2 (Overlays/Glass):** Frosted surfaces that sit "closer" to the user, blurring the content beneath them.

## Shapes

The shape language is dominated by high-radius curves to eliminate visual tension.

- **Corner Radius:** A standard 24px (`rounded-xl` in this system) is used for all main cards, book carousels, and imagery.
- **Decorative Elements:** Include occasional "organic" shapes—abstract floral silhouettes or "sparkle" icons (4-pointed stars)—used as background motifs or icon accents.
- **Image Treatment:** Use a consistent 24px radius for all book covers and hero images to align with the UI containers.

## Components

### Buttons
- **Primary:** Filled with the "Ethereal Flow" gradient, white text, 24px radius, and a subtle drop shadow that glows with the primary pink.
- **Secondary:** Ghost style with a 1.5px border in Rose Pink and an optional soft pink hover fill.
- **AI-Action:** Lavender Purple background with a small sparkle icon suffix.

### Input Fields
- Soft white backgrounds with a subtle pink glow on focus. Place labels above the field in `label-md` typography. Borders should be almost invisible (`#F3F4F6`) until interacted with.

### Cards (The "Book Stack")
- Featured books should appear on white cards with 24px rounded corners.
- Use a slight vertical "float" animation (2-4px) on hover.
- Glassmorphism overlays can be used at the bottom of book covers for titles and authors to ensure legibility.

### Chips & Tags
- Used for genres (e.g., "Romance," "Sci-Fi"). These should be pill-shaped with very light pastel fills (e.g., 10% opacity of the primary color) and dark text.

### Interactive "Sparkles"
- Use micro-animations where the AI is "thinking." Small, 4-pointed stars in Gold (#FBBF24) that subtly pulse or rotate to indicate active AI processing.