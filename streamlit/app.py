import streamlit as st
import os
from lyrics_fetcher import LyricsFetcher
from wordcloud_generator import WordCloudGenerator
import time

# Configure page
st.set_page_config(
    page_title="Taylor Swift Lyrics Word Cloud Generator",
    page_icon="🎵",
    layout="wide"
)

# Initialize components
@st.cache_resource
def get_lyrics_fetcher():
    return LyricsFetcher()

@st.cache_resource
def get_wordcloud_generator():
    return WordCloudGenerator()

def main():
    st.title("🎵 Taylor Swift Lyrics Word Cloud Generator")
    st.markdown("Enter a Taylor Swift song title to fetch lyrics and generate a beautiful word cloud!")
    
    # Initialize session state
    if 'lyrics' not in st.session_state:
        st.session_state.lyrics = None
    if 'song_title' not in st.session_state:
        st.session_state.song_title = ""
    if 'last_searched' not in st.session_state:
        st.session_state.last_searched = ""
    
    # Get API key status
    api_key = os.getenv("GENIUS_API_KEY", "")
    if not api_key:
        st.error("⚠️ Genius API key not found. Please set the GENIUS_API_KEY environment variable.")
        st.info("To get a Genius API key, visit: https://genius.com/api-clients")
        return
    
    # Initialize fetcher and generator
    lyrics_fetcher = get_lyrics_fetcher()
    wordcloud_generator = get_wordcloud_generator()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔍 Song Search")
        
        # Song input
        song_input = st.text_input(
            "Enter Taylor Swift song title:",
            value=st.session_state.song_title,
            placeholder="e.g., Shake It Off, Love Story, Anti-Hero"
        )
        
        # Search button
        search_clicked = st.button("🎵 Fetch Lyrics", type="primary")
        
        # Process search
        if search_clicked and song_input.strip():
            st.session_state.song_title = song_input.strip()
            
            # Only fetch if it's a new search
            if st.session_state.song_title != st.session_state.last_searched:
                with st.spinner(f"Searching for '{st.session_state.song_title}' lyrics..."):
                    try:
                        lyrics = lyrics_fetcher.fetch_lyrics(st.session_state.song_title)
                        if lyrics:
                            st.session_state.lyrics = lyrics
                            st.session_state.last_searched = st.session_state.song_title
                            st.success(f"✅ Found lyrics for '{st.session_state.song_title}'!")
                            st.rerun()
                        else:
                            st.error("❌ No lyrics found. Please check the song title and try again.")
                            st.session_state.lyrics = None
                    except Exception as e:
                        st.error(f"❌ Error fetching lyrics: {str(e)}")
                        st.session_state.lyrics = None
        
        elif search_clicked and not song_input.strip():
            st.warning("⚠️ Please enter a song title.")
    
    with col2:
        st.subheader("📊 Word Cloud Options")
        
        # Word cloud customization options
        max_words = st.slider("Maximum words in word cloud", 50, 200, 100)
        width = st.slider("Width", 400, 800, 600)
        height = st.slider("Height", 300, 600, 400)
        
        background_color = st.selectbox(
            "Background color",
            ["white", "black", "lightblue", "lightpink", "lightgreen", "lightyellow"]
        )
        
        colormap = st.selectbox(
            "Color scheme",
            ["viridis", "plasma", "inferno", "magma", "cool", "hot", "spring", "summer", "autumn", "winter"]
        )
    
    # Display results
    if st.session_state.lyrics:
        st.markdown("---")
        
        # Create tabs for lyrics and word cloud
        tab1, tab2 = st.tabs(["📝 Lyrics", "☁️ Word Cloud"])
        
        with tab1:
            st.subheader(f"Lyrics: {st.session_state.last_searched}")
            
            # Display lyrics in a text area
            st.text_area(
                "Song Lyrics:",
                value=st.session_state.lyrics,
                height=400,
                disabled=True
            )
            
            # Lyrics statistics
            word_count = len(st.session_state.lyrics.split())
            char_count = len(st.session_state.lyrics)
            line_count = len(st.session_state.lyrics.split('\n'))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", word_count)
            with col2:
                st.metric("Characters", char_count)
            with col3:
                st.metric("Lines", line_count)
        
        with tab2:
            st.subheader(f"Word Cloud: {st.session_state.last_searched}")
            
            # Generate word cloud button
            if st.button("🎨 Generate Word Cloud", type="primary"):
                with st.spinner("Generating word cloud..."):
                    try:
                        wordcloud_fig = wordcloud_generator.generate_wordcloud(
                            st.session_state.lyrics,
                            max_words=max_words,
                            width=width,
                            height=height,
                            background_color=background_color,
                            colormap=colormap
                        )
                        
                        if wordcloud_fig:
                            st.pyplot(wordcloud_fig)
                            st.success("✅ Word cloud generated successfully!")
                        else:
                            st.error("❌ Failed to generate word cloud.")
                    except Exception as e:
                        st.error(f"❌ Error generating word cloud: {str(e)}")
    
    # Instructions and tips
    st.markdown("---")
    st.subheader("💡 Tips")
    st.markdown("""
    - **Popular Taylor Swift songs to try:** "Shake It Off", "Love Story", "Anti-Hero", "Blank Space", "22"
    - **Search tips:** Use exact song titles for best results
    - **Word cloud:** Larger words appear more frequently in the lyrics
    - **Customization:** Adjust the word cloud settings to create different visual styles
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Powered by Genius API")

if __name__ == "__main__":
    main()
