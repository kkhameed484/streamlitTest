import streamlit as st
from imdb_otter import IMDbOtter
from pdf_generator import create_talent_pdf

st.set_page_config(page_title="IMDb Talent Report Engine", layout="centered")

st.title("🎬 IMDb Talent Profile Generator")
st.write("Search for an actor or actress to fetch live dataset profiles and compile a PDF document.")

# Initialize the public data stream client
@st.cache_resource
def get_imdb_client():
    return IMDbOtter()

otter = get_imdb_client()

# Search UI Element
search_query = st.text_input("Enter Talent Name (e.g., Tom Hanks, Meryl Streep)", value="Tom Hanks")

if search_query:
    with st.spinner("Querying active datasets..."):
        # Look up talent profile records
        talent_profile = otter.get_person_by_name(search_query)
        
    if talent_profile:
        actor_name = talent_profile.name
        st.subheader(f"Target Selected: {actor_name}")
        
        # Parse biographical snippets safely
        bio_text = talent_profile.biography if hasattr(talent_profile, 'biography') and talent_profile.biography else "Public dataset profile overview verified."
        if len(bio_text) > 600:
            bio_text = bio_text[:600] + "..."
            
        st.markdown(f"**Bio Preview:** {bio_text}")
        
        # Build filmography dictionaries list
        filmography_items = []
        credits_list = talent_profile.get_credits(limit=8) # Cap at top 8 records
        
        for credit in credits_list:
            filmography_items.append({
                'year': getattr(credit, 'year', 'N/A'),
                'title': getattr(credit, 'title', 'Untitled Production'),
                'role': getattr(credit, 'category', 'Cast Member').capitalize()
            })
            
        st.divider()
        
        if st.button("🚀 Compile Vector Layout PDF"):
            with st.spinner("Structuring ReportLab flowable elements..."):
                pdf_stream = create_talent_pdf(
                    actor_name=actor_name,
                    bio_summary=bio_text,
                    filmography_data=filmography_items
                )
                
                st.download_button(
                    label=f"💾 Download {actor_name} PDF Profile",
                    data=pdf_stream,
                    file_name=f"{actor_name.lower().replace(' ', '_')}_profile.pdf",
                    mime="application/pdf"
                )
                st.success("PDF compilation successfully written into memory channel stream!")
    else:
        st.error("No exact matching profiles found. Please verify spelling configurations and retry.")
