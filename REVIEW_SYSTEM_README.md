# Review System & Word Cloud Feature

## Overview

The SymptoScan project now includes a comprehensive review system that allows users to provide feedback on their prediction experiences. The review text data is used to generate a word cloud visualization, providing insights into user sentiment and common themes in feedback.

## Features

### 1. Review System
- **Add Reviews**: Users can submit reviews after completing a prediction
- **Edit Reviews**: Users can modify their existing reviews
- **Delete Reviews**: Users can remove their reviews
- **Star Ratings**: 1-5 star rating system
- **Comments**: Text feedback about the prediction experience
- **Review Display**: Reviews are shown on disease detail pages and home page

### 2. Word Cloud Visualization
- **Dynamic Generation**: Word cloud is generated from all review comments
- **Frequency Analysis**: Word size represents frequency in reviews
- **Stop Word Filtering**: Common words are filtered out for better visualization
- **Statistics**: Shows total reviews, words, and unique words
- **Top Words List**: Displays the 10 most frequent words

## Implementation Details

### Models
- `Review`: Stores user reviews with rating, comment, and timestamps
- `Prediction`: Links reviews to specific predictions
- `Disease`: Associated disease for each review

### Views
- `add_review()`: Handle review submission
- `edit_review()`: Handle review editing
- `delete_review()`: Handle review deletion
- `wordcloud_view()`: Generate and display word cloud

### Templates
- `add_review.html`: Review submission form
- `edit_review.html`: Review editing form
- `wordcloud.html`: Word cloud visualization page
- Updated `home.html`: Shows recent reviews with word cloud link
- Updated `disease_detail.html`: Shows disease-specific reviews

### URLs
- `/review/add/<prediction_id>/`: Add review for a prediction
- `/review/edit/<review_id>/`: Edit existing review
- `/review/delete/<review_id>/`: Delete review
- `/wordcloud/`: View word cloud visualization

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Add Sample Data** (Optional):
   ```bash
   python manage.py add_sample_reviews
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### For Users
1. **Submit a Review**:
   - Complete a disease prediction
   - On the result page, click "Leave a Review"
   - Rate the experience (1-5 stars)
   - Add your feedback comment
   - Submit the review

2. **View Reviews**:
   - Visit any disease detail page to see reviews
   - Check the home page for recent reviews
   - Click "View Review Word Cloud" to see the visualization

3. **Manage Reviews**:
   - Edit your reviews from disease detail pages
   - Delete reviews you no longer want to keep

### For Administrators
1. **Monitor Reviews**:
   - Access reviews through Django admin
   - View word cloud statistics
   - Analyze user feedback patterns

2. **Word Cloud Analysis**:
   - Visit `/wordcloud/` to see the visualization
   - Analyze most frequent words in user feedback
   - Use insights to improve the platform

## Technical Implementation

### Word Cloud Generation
The word cloud is generated using the `wordcloud` Python library:

```python
def generate_wordcloud_data():
    # Get all review comments
    reviews = Review.objects.all()
    
    # Combine and clean text
    all_text = ' '.join([review.comment for review in reviews])
    all_text = re.sub(r'[^\w\s]', '', all_text.lower())
    
    # Filter stop words and count frequencies
    words = [word for word in all_text.split() if word not in stop_words]
    word_freq = Counter(words)
    
    return word_freq
```

### Stop Words
The system filters out common words like:
- Articles: the, a, an
- Pronouns: I, you, he, she, it
- Common verbs: is, are, was, were
- Prepositions: in, on, at, to, for
- And many more to focus on meaningful content

### Security Features
- Users can only edit/delete their own reviews
- CSRF protection on all forms
- Input validation and sanitization
- Rate limiting considerations

## Customization

### Adding New Review Fields
1. Update the `Review` model in `models.py`
2. Modify the `ReviewForm` in `forms.py`
3. Update templates to include new fields
4. Run migrations

### Customizing Word Cloud
1. Modify `generate_wordcloud_data()` function
2. Adjust stop words list
3. Change word cloud parameters (size, colors, etc.)
4. Update the visualization template

### Styling
- All templates use Bootstrap 5 for responsive design
- Custom CSS classes for consistent styling
- Font Awesome icons for visual elements

## Future Enhancements

1. **Sentiment Analysis**: Analyze review sentiment (positive/negative)
2. **Review Moderation**: Admin approval system for reviews
3. **Review Categories**: Categorize reviews by prediction accuracy, ease of use, etc.
4. **Advanced Analytics**: More detailed word cloud analytics
5. **Export Features**: Export review data and word cloud statistics
6. **Real-time Updates**: Live word cloud updates as new reviews are added

## Troubleshooting

### Common Issues
1. **Word Cloud Not Generating**: Check if reviews exist in the database
2. **Import Errors**: Ensure all required packages are installed
3. **Template Errors**: Verify all template files are in the correct locations
4. **Permission Errors**: Check file permissions for image generation

### Debug Mode
Enable Django debug mode to see detailed error messages:
```python
DEBUG = True  # In settings.py
```

## Support

For issues or questions about the review system:
1. Check the Django logs for error messages
2. Verify all dependencies are installed
3. Ensure database migrations are up to date
4. Test with sample data using the management command
