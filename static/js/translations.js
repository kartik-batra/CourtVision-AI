/**
 * CourtVision AI — UI Translations
 * Supported: en (English), hi (Hindi), ta (Tamil)
 */
window.TRANSLATIONS = {
  en: {
    // Navbar
    nav_documents:       "Documents",
    nav_search:          "Search Cases",
    nav_history:         "Research History",
    nav_upload:          "Upload Document",

    // Document list
    page_library:        "Legal Documents",
    eyebrow_library:     "Documents Library",
    btn_upload:          "Upload",
    btn_advanced_search: "Advanced Search",
    label_analysed:      "analysed",
    label_processing:    "processing",
    info_readonly:       "You can view, search, and research all documents. Document upload and deletion are restricted to administrators.",
    filter_all_types:    "All Types",
    filter_all_status:   "All Status",
    filter_newest:       "Newest First",
    filter_oldest:       "Oldest First",
    filter_title_az:     "Title A-Z",
    filter_title_za:     "Title Z-A",
    filter_filing_date:  "Filing Date",
    btn_filter:          "Filter",
    btn_view_summary:    "View Case Details & AI Summary",
    no_docs_title:       "No Documents Yet",
    no_docs_msg:         "Upload the first commercial court document to get started.",
    no_match_title:      "No Matching Documents",
    no_match_msg:        "Try broadening your search criteria.",
    btn_clear_filters:   "Clear Filters",

    // Document detail tabs
    tab_summary:         "AI Summary",
    tab_findings:        "Key Findings",
    tab_metadata:        "Case Details",
    tab_viewer:          "Original Document",
    label_ai_complete:   "AI Analysis Complete",
    label_processing_ai: "AI Analysis in Progress",
    btn_research_query:  "Research Query",
    btn_download:        "Download",
    btn_delete:          "Delete",

    // Summary section
    full_doc_summarised: "Full document summarised using map-reduce pipeline",
    chunks_processed:    "chunks processed",
    words_total:         "words total",
    generated_at:        "Generated",
    groq_powered:        "Groq LLaMA 4 Scout",
    faiss_indexed:       "FAISS Indexed",
    langgraph_label:     "LangGraph",

    // Key findings
    label_principle:     "Principle:",
    no_findings:         "No structured findings were extracted.",

    // Case details
    drop_file:            "Drop your file here or click to browse",
    allowed_files:        "Only PDF files are allowed — Max 10MB",
    label_description:   "Description",
    label_file_upload:   "File *",
    info_upload:         "The document will be processed by our AI engine for summary and research capabilities.",
    label_file:          "Document Details",
    label_title:         "Document Title",
    label_type:          "Type",
    label_case_no:       "Case No.",
    label_court:         "Court",
    label_filed:         "Filed",
    label_size:          "Size",
    label_uploaded:      "Uploaded",
    label_last_updated:  "Last Updated",
    label_status:        "Status",
    label_ai_summary:    "AI Summary",
    label_summary_gen:   "Summary Generated",
    label_vector_store:  "Vector Store",
    label_words:         "Word Count",
    label_chunks:        "AI Chunks Processed",

    // Search page
    eyebrow_search:      "Case Intelligence",
    title_search:        "Search & Browse Cases",
    label_total_cases:   "Total Cases",
    label_ai_analysed:   "AI Analysed",
    filter_keyword:      "Keyword",
    filter_doc_type:     "Document Type",
    filter_status:       "Status",
    filter_court:        "Court",
    filter_filing_date:  "Filing Date",
    filter_sort:         "Sort By",
    filter_all_courts:   "All Courts",
    btn_search:          "Search",
    btn_clear_all:       "Clear All Filters",
    label_all:           "All",
    newest_uploaded:     "Newest Uploaded",
    oldest_uploaded:     "Oldest Uploaded",
    no_cases_title:      "No Cases Found",
    no_cases_msg:        "Try adjusting your filters.",
    btn_research:        "Research",
    ai_ready:            "AI Summary Ready",

    // Research interface
    eyebrow_research:    "AI Research Assistant",
    label_query:         "Research Query",
    query_placeholder:   "Ask a specific legal question about this document...",
    hint_ctrl_enter:     "Ctrl+Enter to submit · Results are saved permanently",
    btn_research_submit: "Research",
    prev_queries_label:  "Previous Queries on This Document",
    btn_full_answer:     "Full Answer",
    btn_re_query:        "Re-query Document",
    tip_title:           "Research Tips",
    tip1:                "Ask about specific parties or dates",
    tip2:                "Query legal principles applied",
    tip3:                "Ask for monetary amounts or relief",
    tip4:                "Request procedural history",
    tip5:                "All answers are saved to history",
    saved_to_history:    "Saved to research history",
    btn_view_full:       "View Full Answer",
    searching_faiss:     "Searching FAISS index and generating answer…",
    source_passages:     "Source Passages (FAISS)",

    // Research history
    eyebrow_history:     "Saved Research",
    title_history:       "Research History",
    subtitle_history:    "Access your queries and AI generated Responses",
    label_total_q:       "Total Queries",
    label_docs_researched: "Documents Researched",
    label_matching:      "Matching",
    label_showing:       "Showing",
    all_docs_filter:     "All Documents",
    sort_newest:         "Newest First",
    sort_oldest:         "Oldest First",
    sort_by_doc:         "By Document",
    no_history_title:    "No Research History Yet",
    no_history_msg:      "Upload a document, run a research query, and it will be saved here permanently.",
    no_match_q_title:    "No Matching Queries",
    no_match_q_msg:      "Try adjusting your search filters.",
    label_saved:         "Saved",
    btn_full_answer_h:   "Full Answer",
    btn_delete:          "Delete",

    // Footer
    footer_platform:     "Platform",
    footer_ai_pipeline:  "AI Pipeline",
    footer_session:      "Session",
    footer_operational:  "System Operational",
    footer_sign_out:     "Sign Out",
    footer_admin:        "Administrator",
    footer_researcher:   "Researcher",

    // Auth pages
    label_username:      "Username",
    label_password:      "Password",
    label_forgot:        "Forgot password?",
    btn_sign_in:         "Sign In to Platform",
    no_account:          "New to CourtVision AI?",
    btn_create_account:  "Create Account",
    label_email:         "Email Address",
    btn_send_reset:      "Send Reset Link",
    remembered_pwd:      "Remembered your password?",
    sign_in_link:        "Sign In",
  },

  hi: {
    // Navbar
    nav_documents:       "दस्तावेज़",
    nav_search:          "केस खोजें",
    nav_history:         "शोध इतिहास",
    nav_upload:          "दस्तावेज़ अपलोड करें",

    // Document list
    page_library:        "कानूनी दस्तावेज़",
    eyebrow_library:     "दस्तावेज़ पुस्तकालय",
    btn_upload:          "अपलोड",
    btn_advanced_search: "उन्नत खोज",
    label_analysed:      "विश्लेषित",
    label_processing:    "प्रक्रिया में",
    info_readonly:       "आप सभी दस्तावेज़ देख, खोज और शोध कर सकते हैं। अपलोड और डिलीट केवल प्रशासकों तक सीमित है।",
    filter_all_types:    "सभी प्रकार",
    filter_all_status:   "सभी स्थिति",
    filter_newest:       "नवीनतम पहले",
    filter_oldest:       "पुराने पहले",
    filter_title_az:     "शीर्षक A-Z",
    filter_title_za:     "शीर्षक Z-A",
    filter_filing_date:  "दाखिल तिथि",
    btn_filter:          "फ़िल्टर",
    btn_view_summary:    "केस विवरण और AI सारांश देखें",
    no_docs_title:       "अभी कोई दस्तावेज़ नहीं",
    no_docs_msg:         "शुरू करने के लिए पहला दस्तावेज़ अपलोड करें।",
    no_match_title:      "कोई मिलान नहीं",
    no_match_msg:        "खोज मानदंड को व्यापक बनाने का प्रयास करें।",
    btn_clear_filters:   "फ़िल्टर साफ़ करें",

    // Document detail tabs
    tab_summary:         "AI सारांश",
    tab_findings:        "मुख्य निष्कर्ष",
    tab_metadata:        "केस विवरण",
    tab_viewer:          "मूल दस्तावेज़",
    label_ai_complete:   "AI विश्लेषण पूर्ण",
    label_processing_ai: "AI विश्लेषण प्रगति में",
    btn_research_query:  "शोध प्रश्न",
    btn_download:        "डाउनलोड",
    btn_delete:          "हटाएं",

    // Summary section
    full_doc_summarised: "पूरा दस्तावेज़ मैप-रिड्यूस पाइपलाइन से सारांशित",
    chunks_processed:    "खंड प्रसंस्कृत",
    words_total:         "कुल शब्द",
    generated_at:        "उत्पन्न",
    groq_powered:        "Groq LLaMA 4 Scout",
    faiss_indexed:       "FAISS अनुक्रमित",
    langgraph_label:     "LangGraph",

    // Key findings
    label_principle:     "सिद्धांत:",
    no_findings:         "कोई संरचित निष्कर्ष नहीं निकाले गए।",

    // Case details
    drop_file:            "अपना फ़ाइल यहाँ ड्रॉप करें या ब्राउज़ करने के लिए क्लिक करें",
    allowed_files:        "केवल PDF फ़ाइलों की अनुमति है — अधिकतम 10MB",
    label_description:   "विवरण",
    label_file_upload:   "फ़ाइल *",
    info_upload:         "दस्तावेज़ हमारे AI इंजन द्वारा सारांश और शोध क्षमताओं के लिए संसाधित किया जाएगा।",
    label_file:          "दस्तावेज़ विवरण",
    label_title:         "दस्तावेज़ शीर्षक",
    label_type:          "प्रकार",
    label_case_no:       "केस नंबर",
    label_court:         "न्यायालय",
    label_filed:         "दायर किया",
    label_size:          "आकार",
    label_uploaded:      "अपलोड किया",
    label_last_updated:  "अंतिम अपडेट",
    label_status:        "स्थिति",
    label_ai_summary:    "AI सारांश",
    label_summary_gen:   "सारांश उत्पन्न",
    label_vector_store:  "वेक्टर स्टोर",
    label_words:         "शब्द गणना",
    label_chunks:        "AI खंड प्रसंस्कृत",

    // Search page
    eyebrow_search:      "केस इंटेलिजेंस",
    title_search:        "केस खोजें और ब्राउज़ करें",
    label_total_cases:   "कुल केस",
    label_ai_analysed:   "AI विश्लेषित",
    filter_keyword:      "कीवर्ड",
    filter_doc_type:     "दस्तावेज़ प्रकार",
    filter_status:       "स्थिति",
    filter_court:        "न्यायालय",
    filter_filing_date:  "दाखिल तिथि",
    filter_sort:         "क्रमबद्ध करें",
    filter_all_courts:   "सभी न्यायालय",
    btn_search:          "खोजें",
    btn_clear_all:       "सभी फ़िल्टर साफ़ करें",
    label_all:           "सभी",
    newest_uploaded:     "नवीनतम अपलोड",
    oldest_uploaded:     "पुराने अपलोड",
    no_cases_title:      "कोई केस नहीं मिला",
    no_cases_msg:        "अपने फ़िल्टर समायोजित करने का प्रयास करें।",
    btn_research:        "शोध",
    ai_ready:            "AI सारांश तैयार",

    // Research interface
    eyebrow_research:    "AI शोध सहायक",
    label_query:         "शोध प्रश्न",
    query_placeholder:   "इस दस्तावेज़ के बारे में एक विशिष्ट कानूनी प्रश्न पूछें...",
    hint_ctrl_enter:     "Ctrl+Enter से सबमिट करें · परिणाम स्थायी रूप से सहेजे जाते हैं",
    btn_research_submit: "शोध करें",
    prev_queries_label:  "इस दस्तावेज़ पर पिछले प्रश्न",
    btn_full_answer:     "पूरा उत्तर",
    btn_re_query:        "पुनः प्रश्न करें",
    tip_title:           "शोध सुझाव",
    tip1:                "विशिष्ट पक्षों या तिथियों के बारे में पूछें",
    tip2:                "लागू कानूनी सिद्धांतों की जांच करें",
    tip3:                "मौद्रिक राशि या राहत के लिए पूछें",
    tip4:                "प्रक्रियात्मक इतिहास का अनुरोध करें",
    tip5:                "सभी उत्तर इतिहास में सहेजे जाते हैं",
    saved_to_history:    "शोध इतिहास में सहेजा गया",
    btn_view_full:       "पूरा उत्तर देखें",
    searching_faiss:     "FAISS इंडेक्स खोजा जा रहा है और उत्तर तैयार हो रहा है...",
    source_passages:     "स्रोत अनुच्छेद (FAISS)",

    // Research history
    eyebrow_history:     "सहेजा गया शोध",
    title_history:       "शोध इतिहास",
    subtitle_history:    "सभी प्रश्न और AI उत्तर स्थायी रूप से संग्रहीत हैं",
    label_total_q:       "कुल प्रश्न",
    label_docs_researched: "शोधित दस्तावेज़",
    label_matching:      "मिलान",
    label_showing:       "दिखाया जा रहा",
    all_docs_filter:     "सभी दस्तावेज़",
    sort_newest:         "नवीनतम पहले",
    sort_oldest:         "पुराने पहले",
    sort_by_doc:         "दस्तावेज़ अनुसार",
    no_history_title:    "अभी कोई शोध इतिहास नहीं",
    no_history_msg:      "एक दस्तावेज़ अपलोड करें और शोध प्रश्न चलाएं।",
    no_match_q_title:    "कोई मिलान नहीं",
    no_match_q_msg:      "अपने फ़िल्टर समायोजित करने का प्रयास करें।",
    label_saved:         "सहेजा",
    btn_full_answer_h:   "पूरा उत्तर",
    btn_delete:          "हटाएं",

    // Footer
    footer_platform:     "प्लेटफ़ॉर्म",
    footer_ai_pipeline:  "AI पाइपलाइन",
    footer_session:      "सत्र",
    footer_operational:  "सिस्टम चालू है",
    footer_sign_out:     "साइन आउट",
    footer_admin:        "प्रशासक",
    footer_researcher:   "शोधकर्ता",

    // Auth pages
    label_username:      "उपयोगकर्ता नाम",
    label_password:      "पासवर्ड",
    label_forgot:        "पासवर्ड भूल गए?",
    btn_sign_in:         "प्लेटफ़ॉर्म में साइन इन करें",
    no_account:          "CourtVision AI में नए हैं?",
    btn_create_account:  "खाता बनाएं",
    label_email:         "ईमेल पता",
    btn_send_reset:      "रीसेट लिंक भेजें",
    remembered_pwd:      "पासवर्ड याद आ गया?",
    sign_in_link:        "साइन इन करें",
  },

  ta: {
    // Navbar
    nav_documents:       "ஆவணங்கள்",
    nav_search:          "வழக்குகளைத் தேடு",
    nav_history:         "ஆராய்ச்சி வரலாறு",
    nav_upload:          "ஆவணம் பதிவேற்று",

    // Document list
    page_library:        "சட்ட ஆவணங்கள்",
    eyebrow_library:     "ஆவண நூலகம்",
    btn_upload:          "பதிவேற்று",
    btn_advanced_search: "மேம்பட்ட தேடல்",
    label_analysed:      "பகுப்பாய்வு செய்யப்பட்டது",
    label_processing:    "செயலாக்கத்தில்",
    info_readonly:       "அனைத்து ஆவணங்களையும் பார்க்கலாம், தேடலாம் மற்றும் ஆராயலாம். பதிவேற்றம் மற்றும் நீக்கம் நிர்வாகிகளுக்கு மட்டுமே.",
    filter_all_types:    "அனைத்து வகைகளும்",
    filter_all_status:   "அனைத்து நிலைகளும்",
    filter_newest:       "புதியது முதலில்",
    filter_oldest:       "பழையது முதலில்",
    filter_title_az:     "தலைப்பு A-Z",
    filter_title_za:     "தலைப்பு Z-A",
    filter_filing_date:  "தாக்கல் தேதி",
    btn_filter:          "வடிகட்டு",
    btn_view_summary:    "வழக்கு விவரங்கள் மற்றும் AI சுருக்கம் பார்க்க",
    no_docs_title:       "இன்னும் ஆவணங்கள் இல்லை",
    no_docs_msg:         "தொடங்க முதல் ஆவணத்தை பதிவேற்றவும்.",
    no_match_title:      "பொருந்தும் ஆவணங்கள் இல்லை",
    no_match_msg:        "தேடல் அளவுகோல்களை விரிவுபடுத்த முயற்சிக்கவும்.",
    btn_clear_filters:   "வடிகட்டிகளை அழி",

    // Document detail tabs
    tab_summary:         "AI சுருக்கம்",
    tab_findings:        "முக்கிய கண்டுபிடிப்புகள்",
    tab_metadata:        "வழக்கு விவரங்கள்",
    tab_viewer:          "அசல் ஆவணம்",
    label_ai_complete:   "AI பகுப்பாய்வு முடிந்தது",
    label_processing_ai: "AI பகுப்பாய்வு நடைபெறுகிறது",
    btn_research_query:  "ஆராய்ச்சி கேள்வி",
    btn_download:        "பதிவிறக்கு",
    btn_delete:          "நீக்கு",

    // Summary section
    full_doc_summarised: "முழு ஆவணம் மேப்-ரிடியூஸ் பைப்லைன் மூலம் சுருக்கப்பட்டது",
    chunks_processed:    "பகுதிகள் செயலாக்கப்பட்டன",
    words_total:         "மொத்த வார்த்தைகள்",
    generated_at:        "உருவாக்கப்பட்டது",
    groq_powered:        "Groq LLaMA 4 Scout",
    faiss_indexed:       "FAISS அட்டவணையிடப்பட்டது",
    langgraph_label:     "LangGraph",

    // Key findings
    label_principle:     "கொள்கை:",
    no_findings:         "கட்டமைக்கப்பட்ட கண்டுபிடிப்புகள் எதுவும் இல்லை.",

    // Case details
    drop_file:            "உங்கள் கோப்பை இங்கே விடவும் அல்லது உலாவுவதற்கு கிளிக் करें",
    allowed_files:        "PDF கோப்புகளுக்கு மட்டுமே அனுமதி - அதிகபட்சம் 10MB",
    label_description:   "விவரம்",
    label_file_upload:   "ஆவணம் *",
    info_upload:         "ஆவணம் சுருக்கம் மற்றும் ஆராய்ச்சி திறன்களுக்காக எங்கள் AI இயந்திரத்தால் செயலாக்கப்படும்.",
    label_file:          "ஆவண விவரங்கள்",
    label_title:         "ஆவண தலைப்பு",
    label_type:          "வகை",
    label_case_no:       "வழக்கு எண்",
    label_court:         "நீதிமன்றம்",
    label_filed:         "தாக்கல் செய்யப்பட்டது",
    label_size:          "அளவு",
    label_uploaded:      "பதிவேற்றப்பட்டது",
    label_last_updated:  "கடைசியாக புதுப்பிக்கப்பட்டது",
    label_status:        "நிலை",
    label_ai_summary:    "AI சுருக்கம்",
    label_summary_gen:   "சுருக்கம் உருவாக்கப்பட்டது",
    label_vector_store:  "வெக்டர் ஸ்டோர்",
    label_words:         "வார்த்தை எண்ணிக்கை",
    label_chunks:        "AI பகுதிகள் செயலாக்கப்பட்டன",

    // Search page
    eyebrow_search:      "வழக்கு புலனாய்வு",
    title_search:        "வழக்குகளைத் தேடு மற்றும் உலாவு",
    label_total_cases:   "மொத்த வழக்குகள்",
    label_ai_analysed:   "AI பகுப்பாய்வு",
    filter_keyword:      "முக்கிய வார்த்தை",
    filter_doc_type:     "ஆவண வகை",
    filter_status:       "நிலை",
    filter_court:        "நீதிமன்றம்",
    filter_filing_date:  "தாக்கல் தேதி",
    filter_sort:         "வரிசைப்படுத்து",
    filter_all_courts:   "அனைத்து நீதிமன்றங்களும்",
    btn_search:          "தேடு",
    btn_clear_all:       "அனைத்து வடிகட்டிகளையும் அழி",
    label_all:           "அனைத்தும்",
    newest_uploaded:     "புதிதாக பதிவேற்றப்பட்டது",
    oldest_uploaded:     "பழைய பதிவேற்றம்",
    no_cases_title:      "வழக்குகள் இல்லை",
    no_cases_msg:        "உங்கள் வடிகட்டிகளை சரிசெய்ய முயற்சிக்கவும்.",
    btn_research:        "ஆராய்",
    ai_ready:            "AI சுருக்கம் தயார்",

    // Research interface
    eyebrow_research:    "AI ஆராய்ச்சி உதவியாளர்",
    label_query:         "ஆராய்ச்சி கேள்வி",
    query_placeholder:   "இந்த ஆவணத்தைப் பற்றி ஒரு குறிப்பிட்ட சட்டக் கேள்வி கேளுங்கள்...",
    hint_ctrl_enter:     "Ctrl+Enter மூலம் சமர்ப்பிக்கவும் · முடிவுகள் நிரந்தரமாக சேமிக்கப்படுகின்றன",
    btn_research_submit: "ஆராய்",
    prev_queries_label:  "இந்த ஆவணத்தில் முந்தைய கேள்விகள்",
    btn_full_answer:     "முழு பதில்",
    btn_re_query:        "மீண்டும் கேளுங்கள்",
    tip_title:           "ஆராய்ச்சி குறிப்புகள்",
    tip1:                "குறிப்பிட்ட கட்சிகள் அல்லது தேதிகளைப் பற்றி கேளுங்கள்",
    tip2:                "பயன்படுத்தப்பட்ட சட்டக் கொள்கைகளை விசாரிக்கவும்",
    tip3:                "பணத் தொகை அல்லது நிவாரணம் கேளுங்கள்",
    tip4:                "நடைமுறை வரலாற்றை கோருங்கள்",
    tip5:                "அனைத்து பதில்களும் வரலாற்றில் சேமிக்கப்படுகின்றன",
    saved_to_history:    "ஆராய்ச்சி வரலாற்றில் சேமிக்கப்பட்டது",
    btn_view_full:       "முழு பதில் பார்க்க",
    searching_faiss:     "FAISS குறியீட்டில் தேடுகிறது மற்றும் பதில் உருவாக்குகிறது...",
    source_passages:     "மூல பகுதிகள் (FAISS)",

    // Research history
    eyebrow_history:     "சேமித்த ஆராய்ச்சி",
    title_history:       "ஆராய்ச்சி வரலாறு",
    subtitle_history:    "அனைத்து கேள்விகளும் AI பதில்களும் நிரந்தரமாக சேமிக்கப்படுகின்றன",
    label_total_q:       "மொத்த கேள்விகள்",
    label_docs_researched: "ஆராய்ந்த ஆவணங்கள்",
    label_matching:      "பொருந்துவது",
    label_showing:       "காட்டுகிறது",
    all_docs_filter:     "அனைத்து ஆவணங்களும்",
    sort_newest:         "புதியது முதலில்",
    sort_oldest:         "பழையது முதலில்",
    sort_by_doc:         "ஆவணம் வாரியாக",
    no_history_title:    "இன்னும் ஆராய்ச்சி வரலாறு இல்லை",
    no_history_msg:      "ஒரு ஆவணத்தை பதிவேற்றி ஆராய்ச்சி கேள்வி இயக்கவும்.",
    no_match_q_title:    "பொருந்தும் கேள்விகள் இல்லை",
    no_match_q_msg:      "உங்கள் வடிகட்டிகளை சரிசெய்ய முயற்சிக்கவும்.",
    label_saved:         "சேமிக்கப்பட்டது",
    btn_full_answer_h:   "முழு பதில்",
    btn_delete:          "நீக்கு",

    // Footer
    footer_platform:     "தளம்",
    footer_ai_pipeline:  "AI பைப்லைன்",
    footer_session:      "அமர்வு",
    footer_operational:  "கணினி இயங்குகிறது",
    footer_sign_out:     "வெளியேறு",
    footer_admin:        "நிர்வாகி",
    footer_researcher:   "ஆராய்ச்சியாளர்",

    // Auth pages
    label_username:      "பயனர்பெயர்",
    label_password:      "கடவுச்சொல்",
    label_forgot:        "கடவுச்சொல் மறந்தீர்களா?",
    btn_sign_in:         "தளத்தில் உள்நுழை",
    no_account:          "CourtVision AI-ல் புதியவரா?",
    btn_create_account:  "கணக்கு உருவாக்கு",
    label_email:         "மின்னஞ்சல் முகவரி",
    btn_send_reset:      "மீட்டமை இணைப்பை அனுப்பு",
    remembered_pwd:      "கடவுச்சொல் நினைவுக்கு வந்ததா?",
    sign_in_link:        "உள்நுழை",
  }
};

/**
 * Apply translations to the current page.
 * Elements are tagged with data-i18n="key" attributes.
 * Placeholders use data-i18n-placeholder="key".
 */
window.applyTranslations = function(lang) {
  const t = window.TRANSLATIONS[lang] || window.TRANSLATIONS['en'];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.textContent = t[key];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (t[key]) el.title = t[key];
  });
  // Update html lang attribute
  document.documentElement.lang = lang === 'hi' ? 'hi' : lang === 'ta' ? 'ta' : 'en';
  // Persist in localStorage for immediate reload consistency
  localStorage.setItem('court_lang', lang);
};

// Auto-apply on page load using server-set language
document.addEventListener('DOMContentLoaded', () => {
  const lang = window.COURT_LANG || localStorage.getItem('court_lang') || 'en';
  window.applyTranslations(lang);
});
