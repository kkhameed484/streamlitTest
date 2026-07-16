import streamlit as st
from imdb import Cinemagoer
from pdf_generator import create_talent_pdf

st.set_page_config(page_title="IMDb Talent Report Engine", layout="centered")

st.title("🎬 IMDb Talent Profile Generator")
st.write("Search for an actor or actress to fetch live data from IMDb and generate a professional profile report.")

# Initialize the API client
@st.cache_resource
def get_imdb_client():
    return Cinemagoer()

ia = get_imdb_client()

# Search UI Element
search_query = st.text_input("Enter Talent Name (e.g., Tom Hanks, Meryl Streep)", value="Tom Hanks")

if search_query:
    with st.spinner("Searching IMDb database archives..."):
        # Find matching people profiles
        search_results = ia.search_person(search_query)
        
    if search_results:
        # Pick the top logical match from search results
        chosen_person = search_results[0]
        person_id = chosen_person.personID
        
        with st.spinner(f"Retrieving full profile metadata for ID: {person_id}..."):
            # Fetch complete deep details (biography and filmography)
            person_data = ia.get_person(person_id, info=['main', 'biography', 'filmography'])
            
        # Parse the raw name mapping safely
        actor_name = person_data.get('name', 'Unknown Artist')
        st.subheader(f"Target Selected: {actor_name}")
        
        # Safely parse biography text snippet
        bios = person_data.get('biography', [])
        bio_text = bios[0] if isinstance(bios, list) and bios else "No public biography details found on file."
        # Truncate overly long text fields for cleaner visibility
        if len(bio_text) > 600:
            bio_text = bio_text[:600] + "..."
            
        st.markdown(f"**Bio Preview:** {bio_text}")
        
        # Process and structure top 8 clean filmography records
        filmography_items = []
        raw_filmography = person_data.get('filmography', {})
        
        # Look across acting/actress category buckets dynamically
        acting_key = 'actor' if 'actor' in raw_filmography else 'actress'
        project_list = raw_filmography.get(acting_key, [])[:8] # Target top 8 records
        
        for project in project_list:
            filmography_items.append({
                'year': project.get('year', 'N/A'),
                'title': project.get('title', 'Untitled Project'),
                'role': acting_key.capitalize()
            })
            
        st.divider()
        
        # Trigger report assembly when button action is confirmed
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
        st.error("No matches found for that name. Please check spelling configurations and try again.")
