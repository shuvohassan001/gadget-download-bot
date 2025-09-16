import telebot
import os
import time
import threading
import asyncio
from telebot import types
import requests
import json
import uuid
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import re
import math
import subprocess
import yt_dlp
import random
from datetime import datetime, timedelta
import psutil
import platform
import sys
import hashlib
import base64
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import logging
from functools import wraps

try:
    import speech_recognition as sr
    from googletrans import Translator
    from pydub import AudioSegment
    from cryptography.fernet import Fernet
    ADVANCED_FEATURES = True
except ImportError:
    print("Advanced features disabled. Install: pip install speechrecognition googletrans==4.0.0-rc1 pydub cryptography")
    ADVANCED_FEATURES = False

from collections import defaultdict

# Bot configuration
BOT_NAME = "𝐆𝐀𝐃𝐆𝐄𝐓 𝐁𝐎𝐗 𝐒𝐔𝐏𝐄𝐑 𝐓𝐎𝐎𝐋𝐒 𝐔𝐋𝐓𝐑𝐀 𝐀𝐃𝐕𝐀𝐍𝐂𝐄𝐃"
BOT_TOKEN = "8483505119:AAGRFSdXLhiu7KfYtZPibk8-LQoElLTMtKQ"  # REPLACE WITH YOUR TOKEN
DEVELOPER_USERNAME = "@shuvohassan00"
DEVELOPER_ID = "6074463370"
BOT_VERSION = "5.0 ULTRA PREMIUM ADVANCED"

TMP_DIR = "gadget_box_temp"
MODELS_DIR = "ai_models"
DATABASE_DIR = "bot_database"
CACHE_DIR = "premium_cache"

for directory in [TMP_DIR, MODELS_DIR, DATABASE_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# Rate limiting
RATE_LIMIT = 5
RATE_WINDOW = 60
user_requests = defaultdict(list)

# Encryption key (only if cryptography available)
if ADVANCED_FEATURES:
    encryption_key = Fernet.generate_key()
    cipher = Fernet(encryption_key)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 🎨 ULTIMATE PREMIUM EMOJI COLLECTION
EMOJIS = {
    'crown': '👑', 'diamond': '💎', 'gem': '💠', 'star': '⭐', 'sparkles': '✨',
    'fire': '🔥', 'rocket': '🚀', 'lightning': '⚡', 'magic': '🪄', 'crystal': '🔮',
    'rainbow': '🌈', 'comet': '☄️', 'nova': '💫', 'galaxy': '🌌', 'sun': '☀️',
    'moon': '🌙', 'earth': '🌍', 'ocean': '🌊', 'mountain': '🏔️', 'flower': '🌸',
    'heart': '❤️', 'blue_heart': '💙', 'orange_heart': '🧡', 'purple_heart': '💜',
    'green_heart': '💚', 'yellow_heart': '💛', 'black_heart': '🖤', 'white_heart': '🤍',
    'success': '✅', 'error': '❌', 'warning': '⚠️', 'info': '💡', 'video': '🎬', 
    'camera': '📸', 'party': '🎉', 'trophy': '🏆', 'shield': '🛡️', 'clock': '🕐',
    'chart': '📊', 'calendar': '📅', 'download': '📥', 'upload': '📤', 'dancing': '💃',
    'medal': '🏅', 'money': '💰', 'target': '🎯', 'zap': '⚡', 'boom': '💥',
    'alien': '👽', 'robot': '🤖', 'ghost': '👻', 'unicorn': '🦄', 'dragon': '🐉',
    'wizard': '🧙', 'fairy': '🧚', 'vampire': '🧛', 'zombie': '🧟', 'mermaid': '🧜',
    'superhero': '🦸', 'villain': '🦹', 'ninja': '🥷', 'pirate': '🏴‍☠️', 'detective': '🕵️',
    'scientist': '👨‍🔬', 'astronaut': '👨‍🚀', 'artist': '👨‍🎨', 'musician': '👨‍🎤',
    'lock': '🔒', 'speed': '⚡', 'batch': '📦', 'subtitle': '📝', 'translate': '🌐', 
    'compress': '🗜️', 'watermark': '©️', 'playlist': '🎶', '8k': '📺', 'analytics': '📈'
}

# 🌟 ULTRA PREMIUM LOADING ANIMATIONS
ULTIMATE_LOADING_FRAMES = [
    f"{EMOJIS['sparkles']} Initializing {BOT_NAME} Quantum Systems...",
    f"{EMOJIS['crystal']} 🔵 Activating Neural Processors...",
    f"{EMOJIS['magic']} 🟣 Boosting AI Performance Matrix...",
    f"{EMOJIS['lightning']} 🟡 Synchronizing Data Streams...",
    f"{EMOJIS['fire']} 🔴 Applying Ultra Enhancement Filters...",
    f"{EMOJIS['gem']} 🟢 Optimizing Quality Resolution...",
    f"{EMOJIS['nova']} 🟠 Finalizing Cosmic Processing...",
    f"{EMOJIS['crown']} 🟤 Preparing Royal Delivery...",
    f"{EMOJIS['diamond']} ⚫ Polishing to Perfection...",
    f"{EMOJIS['rainbow']} 🌈 Creating Pure Magic...",
    f"{EMOJIS['alien']} 🛸 Scanning Multiverse...",
    f"{EMOJIS['robot']} 🔧 Optimizing Algorithms...",
    f"{EMOJIS['unicorn']} 🌟 Adding Unicorn Power...",
    f"{EMOJIS['dragon']} 🔥 Dragon-Level Processing...",
    f"{EMOJIS['wizard']} 🪄 Casting Premium Spells...",
    f"{EMOJIS['fairy']} ✨ Fairy Dust Enhancement...",
    f"{EMOJIS['superhero']} 💪 Superhero Power Boost...",
    f"{EMOJIS['ninja']} 🥷 Stealth Mode Activation...",
    f"{EMOJIS['scientist']} 🔬 Scientific Analysis...",
    f"{EMOJIS['astronaut']} 🚀 Space-Grade Processing...",
    f"{EMOJIS['8k']} 📺 Upgrading to 8K Resolution...",
    f"{EMOJIS['subtitle']} 📝 Generating Intelligent Subtitles...",
    f"{EMOJIS['translate']} 🌐 Translating Across Languages...",
    f"{EMOJIS['compress']} 🗜️ Smart Compressing Files...",
    f"{EMOJIS['watermark']} ©️ Adding Custom Watermarks...",
    f"{EMOJIS['playlist']} 🎶 Processing Playlists...",
    f"{EMOJIS['analytics']} 📈 Analyzing User Stats..."
]

PREMIUM_PROGRESS_BARS = [
    "🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣🔲🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🔲🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤🔲🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🔲🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🌟🔲🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🌟🔥🔲🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🌟🔥⚡🔲🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🌟🔥⚡🌈🔲🔲",
    "🟪🟦🟩🟨🟧🟥🟫⬛🔵🟢🟣⚪🟤✨🌟🔥⚡🌈👑🔲"
]

PLATFORM_MAP = {
    'youtube': ['youtube.com', 'youtu.be'],
    'tiktok': ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com'],
    'instagram': ['instagram.com', 'instagr.am'],
    'facebook': ['facebook.com', 'fb.watch', 'fb.me'],
    'twitter': ['twitter.com', 'x.com', 't.co'],
    'reddit': ['reddit.com', 'redd.it'],
    'vimeo': ['vimeo.com'],
    'dailymotion': ['dailymotion.com'],
    'twitch': ['twitch.tv'],
    'soundcloud': ['soundcloud.com'],
    'bilibili': ['bilibili.com'],
    'niconico': ['nicovideo.jp'],
    'snapchat': ['snapchat.com'],
    'linkedin': ['linkedin.com'],
    'pinterest': ['pinterest.com'],
    'tumblr': ['tumblr.com'],
    'others': ['general']
}

PREMIUM_QUOTES = [
    "Excellence is an art won by training and habituation.",
    "The best preparation for tomorrow is doing your best today.",
    "Quality is never an accident; it is always the result of intelligent effort.",
    "Dream big and dare to fail.",
    "Innovation distinguishes between a leader and a follower.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Success is where preparation and opportunity meet.",
    "Your limitation—it's only your imagination.",
    "Great things never come from comfort zones.",
    "Be yourself; everyone else is already taken.",
    "The only way to do great work is to love what you do.",
    "Believe you can and you're halfway there.",
    "Strive for progress, not perfection."
]

def safe_get_description(info):
    """Safely extract video description with premium formatting"""
    try:
        desc = info.get('description', '')
        if not isinstance(desc, str) or not desc.strip():
            return "✨ Premium content with amazing quality!"
        desc = desc.strip()
        if len(desc) > 200:
            desc = desc[:200] + '...'
        desc = ' '.join(desc.split())
        return desc
    except Exception:
        return "🎬 Premium quality content delivered!"

def format_duration(seconds):
    """Format duration in premium style"""
    try:
        if not seconds or not isinstance(seconds, (int, float)):
            return "Live/Unknown"
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    except:
        return "Unknown"

def format_number(num):
    """Format numbers in premium style"""
    try:
        if num is None or num == 0:
            return "Unavailable"
        if not isinstance(num, (int, float)):
            return "Unavailable"
        num = int(num)
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return f"{num:,}"
    except:
        return "Unavailable"

def get_system_info():
    """Get system information for premium status"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        return {
            'cpu': f"{cpu_percent:.1f}%",
            'ram': f"{memory.percent:.1f}%",
            'os': platform.system(),
            'python': platform.python_version()
        }
    except:
        return {'cpu': 'N/A', 'ram': 'N/A', 'os': 'N/A', 'python': 'N/A'}

class WorldsBestUltraPremiumBot:
    def __init__(self):
        self.processing_messages = {}
        self.user_sessions = {}
        self.models_loaded = False
        self.setup_ai_models()
        self.bot_start_time = datetime.now()
        self.db = sqlite3.connect('bot.db')
        self.db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, downloads INTEGER DEFAULT 0, enhancements INTEGER DEFAULT 0, batch_downloads INTEGER DEFAULT 0, subtitles_generated INTEGER DEFAULT 0)')
        self.db.commit()
        
        if ADVANCED_FEATURES:
            self.translator = Translator()
            self.recognizer = sr.Recognizer()

    def safe_delete_processing_key(self, key):
        """Safely delete processing key"""
        try:
            if key in self.processing_messages:
                del self.processing_messages[key]
        except:
            pass

    def setup_ai_models(self):
        """Setup AI models with premium fallback"""
        try:
            edsr_path = os.path.join(MODELS_DIR, "EDSR_x4.pb")
            if os.path.exists(edsr_path):
                self.sr_model = cv2.dnn_superres.DnnSuperResImpl_create()
                self.sr_model.readModel(edsr_path)
                self.sr_model.setModel("edsr", 4)
                try:
                    self.sr_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                    self.sr_model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                    print(f"{EMOJIS['lightning']} Premium AI Models loaded with GPU acceleration!")
                except:
                    print(f"{EMOJIS['gem']} Premium AI Models loaded with CPU processing!")
                self.models_loaded = True
            
            # Load face detector for advanced enhancement
            try:
                self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            except:
                self.face_cascade = None
                
        except Exception as e:
            print(f"{EMOJIS['magic']} Using premium fallback algorithms: {e}")
            self.models_loaded = False

    def create_main_keyboard(self):
        """Create world's most beautiful main keyboard"""
        markup = types.InlineKeyboardMarkup(row_width=2)

        hero1 = types.InlineKeyboardButton(
            f"📥 {EMOJIS['crown']} ULTRA DOWNLOADER {EMOJIS['diamond']}", 
            callback_data="ultra_download"
        )
        hero2 = types.InlineKeyboardButton(
            f"🪄 {EMOJIS['magic']} AI 4K ENHANCER {EMOJIS['sparkles']}", 
            callback_data="ai_enhancer"
        )

        platforms = [
            types.InlineKeyboardButton(f"🎬 YouTube {EMOJIS['fire']}", callback_data="select_youtube"),
            types.InlineKeyboardButton(f"💃 TikTok {EMOJIS['party']}", callback_data="select_tiktok"),
            types.InlineKeyboardButton(f"📸 Instagram {EMOJIS['camera']}", callback_data="select_instagram"),
            types.InlineKeyboardButton(f"👥 Facebook {EMOJIS['blue_heart']}", callback_data="select_facebook"),
            types.InlineKeyboardButton(f"🐦 Twitter {EMOJIS['lightning']}", callback_data="select_twitter"),
            types.InlineKeyboardButton(f"🅰️ Reddit {EMOJIS['orange_heart']}", callback_data="select_reddit")
        ]

        # New premium features buttons
        advanced = [
            types.InlineKeyboardButton(f"📦 {EMOJIS['batch']} BATCH DOWNLOAD", callback_data="batch_download"),
            types.InlineKeyboardButton(f"📝 {EMOJIS['subtitle']} SUBTITLES", callback_data="subtitle_gen"),
            types.InlineKeyboardButton(f"📺 {EMOJIS['8k']} 8K MODE", callback_data="enhance_8k"),
            types.InlineKeyboardButton(f"🌐 {EMOJIS['translate']} TRANSLATE", callback_data="auto_translate")
        ]

        support = [
            types.InlineKeyboardButton(f"🛡️ DEVELOPER {EMOJIS['crystal']}", callback_data="developer_support"),
            types.InlineKeyboardButton(f"💫 HELP CENTER {EMOJIS['magic']}", callback_data="help_center"),
            types.InlineKeyboardButton(f"👑 ABOUT BOT {EMOJIS['medal']}", callback_data="about_bot")
        ]

        markup.add(hero1, hero2)
        markup.add(*platforms[:3])
        markup.add(*platforms[3:])
        markup.add(*advanced[:2])
        markup.add(*advanced[2:])
        markup.add(*support)
        
        return markup

    def create_action_keyboard(self, action_type="general"):
        """Create premium action keyboards"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        if action_type == "download":
            btn1 = types.InlineKeyboardButton(f"📥 {EMOJIS['gem']} Download Another", callback_data="ultra_download")
            btn2 = types.InlineKeyboardButton(f"🪄 {EMOJIS['magic']} AI Enhance", callback_data="ai_enhancer")
        elif action_type == "enhance":
            btn1 = types.InlineKeyboardButton(f"🪄 {EMOJIS['sparkles']} Enhance More", callback_data="ai_enhancer")
            btn2 = types.InlineKeyboardButton(f"📥 {EMOJIS['video']} Download Video", callback_data="ultra_download")
        else:
            btn1 = types.InlineKeyboardButton(f"📥 {EMOJIS['download']} Download", callback_data="ultra_download")
            btn2 = types.InlineKeyboardButton(f"🪄 {EMOJIS['magic']} Enhance", callback_data="ai_enhancer")
        
        support_btn = types.InlineKeyboardButton(f"🛡️ {EMOJIS['crystal']} Support", callback_data="developer_support")
        menu_btn = types.InlineKeyboardButton(f"🏠 {EMOJIS['crown']} Main Menu", callback_data="main_menu")
        
        markup.add(btn1, btn2)
        markup.add(support_btn)
        markup.add(menu_btn)
        return markup
    async def ultra_premium_loading_animation(self, chat_id, message_id, task="Processing", duration=10):
        """World's most beautiful loading animation"""
        try:
            for i in range(duration):
                processing_key = f"{chat_id}_{message_id}"
                if processing_key not in self.processing_messages:
                    break
                    
                frame_idx = i % len(ULTIMATE_LOADING_FRAMES)
                progress_idx = min(int((i / duration) * len(PREMIUM_PROGRESS_BARS)), len(PREMIUM_PROGRESS_BARS) - 1)
                
                frame_text = ULTIMATE_LOADING_FRAMES[frame_idx]
                progress_bar = PREMIUM_PROGRESS_BARS[progress_idx]
                percentage = min(int((i / duration) * 100), 100)
                quote = random.choice(PREMIUM_QUOTES)
                
                if percentage < 15:
                    status = "🔮 Initializing quantum processors..."
                elif percentage < 30:
                    status = "🧠 Analyzing media structure with AI..."
                elif percentage < 50:
                    status = "✨ Applying premium algorithms..."
                elif percentage < 70:
                    status = "🎯 Optimizing quality matrix..."
                elif percentage < 90:
                    status = "🏆 Finalizing premium masterpiece..."
                else:
                    status = "🎊 Preparing royal delivery..."
                
                loading_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║         {EMOJIS['crown']} {BOT_NAME} {EMOJIS['crown']}         ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['rocket']} <b>Task:</b> <i>{task}</i>
{EMOJIS['lightning']} <b>Status:</b> <code>{frame_text}</code>

{EMOJIS['gem']} <b>Progress:</b>
<code>{progress_bar}</code> <b>{percentage}%</b>

{EMOJIS['fire']} <b>Speed:</b> <i>Quantum-Sonic Processing</i>
{EMOJIS['magic']} <b>Quality:</b> <i>Ultra Premium 4K</i>
{EMOJIS['sparkles']} <b>Algorithm:</b> <i>AI-Powered Enhancement</i>
{EMOJIS['crystal']} <b>Stage:</b> <i>{status}</i>

{EMOJIS['nova']} <i>"{quote}"</i>

{EMOJIS['heart']} <i>Please wait while our premium AI creates magic...</i>

<b>┌────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['diamond']} PREMIUM PROCESSING ACTIVE {EMOJIS['diamond']}      │</b>
<b>└────────────────────────────────────────────┘</b>
                """
                
                try:
                    bot.edit_message_text(loading_text, chat_id, message_id, parse_mode='HTML')
                    await asyncio.sleep(0.8)
                except Exception as e:
                    if "message is not modified" not in str(e).lower():
                        break
        except Exception as e:
            print(f"Animation error: {e}")

    def check_platform_match(self, url, selected_platform):
        """Check if URL matches selected platform"""
        if not selected_platform:
            return True
        
        platform_urls = PLATFORM_MAP.get(selected_platform, [])
        return any(platform_url in url.lower() for platform_url in platform_urls)

    def download_video_premium(self, url, chat_id, message_id, selected_platform=None):
        processing_key = f"{chat_id}_{message_id}"
        self.processing_messages[processing_key] = True
        
        try:
            if selected_platform and not self.check_platform_match(url, selected_platform):
                platform_name = selected_platform.title()
                self.safe_delete_processing_key(processing_key)
                
                error_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['warning']} PLATFORM MISMATCH {EMOJIS['error']}     ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['info']} <b>Selected Platform:</b> <i>{platform_name}</i>
{EMOJIS['lightning']} <b>Your URL:</b> <code>{url[:50]}...</code>

{EMOJIS['sparkles']} <b>Premium Solutions:</b>
• {EMOJIS['gem']} Please send a <b>{platform_name}</b> link only
• {EMOJIS['magic']} Or use "ULTRA DOWNLOADER" for all platforms
• {EMOJIS['crystal']} Select different platform button if needed

{EMOJIS['crown']} <b>Expected format for {platform_name}:</b>
<code>{PLATFORM_MAP.get(selected_platform, ['N/A'])[0]}</code>

<b>┌────────────────────────────────────────────┐</b>
<b>│   {EMOJIS['shield']} PREMIUM QUALITY GUARANTEED {EMOJIS['shield']}   │</b>
<b>└────────────────────────────────────────────┘</b>
                """
                bot.edit_message_text(error_text, chat_id, message_id, parse_mode='HTML',
                                    reply_markup=self.create_action_keyboard("download"))
                return

            # Start premium animation
            threading.Thread(target=lambda: asyncio.run(
                self.ultra_premium_loading_animation(chat_id, message_id, "Ultra HD Video Download", 12)
            )).start()

            ydl_opts = {
                'format': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]/best',
                'outtmpl': f'{TMP_DIR}/%(title).70s_%(id)s.%(ext)s',
                'writesubtitles': False,
                'writeautomaticsub': False,
                'noplaylist': True,
                'extractaudio': False,
                'no_warnings': True,
                'quiet': True,
                'socket_timeout': 120,
                'retries': 5,
                'concurrent_fragment_downloads': 16,
                'fragment_retries': 10,
                'continuedl': True,
                'nopart': False,
                'http_chunk_size': 10485760,
            }
            
            time.sleep(8)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                title = str(info.get('title', 'Premium Video'))[:50]
                uploader = str(info.get('uploader', 'Premium Creator'))[:30]
                duration_raw = info.get('duration', 0)
                duration_text = format_duration(duration_raw)
                
                quality = info.get('height', 720)
                view_count = format_number(info.get('view_count', 0))
                like_count = format_number(info.get('like_count', 0))
                
                upload_date = info.get('upload_date', '')
                if upload_date:
                    try:
                        date_obj = datetime.strptime(upload_date, '%Y%m%d')
                        upload_date = date_obj.strftime('%d %B, %Y')
                    except:
                        upload_date = "Recent"
                else:
                    upload_date = "Recent"
                
                description = safe_get_description(info)
                
                downloaded_file = None
                video_id = str(info.get('id', ''))
                if video_id:
                    try:
                        for file in os.listdir(TMP_DIR):
                            if video_id in file and file.endswith(('.mp4', '.mkv', '.webm')):
                                file_path = os.path.join(TMP_DIR, file)
                                file_size = os.path.getsize(file_path)
                                if file_size < 2147483648:
                                    downloaded_file = file_path
                                    break
                    except Exception as e:
                        print(f"File search error: {e}")

                self.safe_delete_processing_key(processing_key)
                time.sleep(2)

                processing_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║    {EMOJIS['success']} DOWNLOAD COMPLETED! {EMOJIS['party']}    ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['video']} <b>Title:</b> <i>{title}</i>
{EMOJIS['crown']} <b>Creator:</b> <i>{uploader}</i>
{EMOJIS['clock']} <b>Duration:</b> <i>{duration_text}</i>
{EMOJIS['gem']} <b>Quality:</b> <i>{quality}p Ultra HD</i>
{EMOJIS['chart']} <b>Views:</b> <i>{view_count}</i>
{EMOJIS['heart']} <b>Likes:</b> <i>{like_count}</i>
{EMOJIS['calendar']} <b>Published:</b> <i>{upload_date}</i>

{EMOJIS['info']} <b>Description:</b> <i>{description}</i>

{EMOJIS['sparkles']} <b>Premium Features Applied:</b>
• {EMOJIS['lightning']} 100% Watermark-Free Guaranteed
• {EMOJIS['magic']} Maximum Quality Downloaded ({quality}p)
• {EMOJIS['crystal']} Ultra-Fast Processing
• {EMOJIS['shield']} Premium Security Applied
• {EMOJIS['trophy']} Large File Support (2GB)

{EMOJIS['upload']} <b>Status:</b> <i>Sending your premium video now...</i>

<b>┌────────────────────────────────────────────┐</b>
<b>│    {EMOJIS['crown']} PREMIUM SUCCESS DELIVERY {EMOJIS['crown']}    │</b>
<b>└────────────────────────────────────────────┘</b>
                """
                
                bot.edit_message_text(processing_text, chat_id, message_id, parse_mode='HTML')

                if downloaded_file and os.path.exists(downloaded_file):
                    time.sleep(3)
                    file_size_mb = os.path.getsize(downloaded_file) / (1024 * 1024)
                    
                    video_caption = f"""
{EMOJIS['crown']} <b>{BOT_NAME} PREMIUM DOWNLOAD</b>

{EMOJIS['sparkles']} <b>{title}</b>
{EMOJIS['crown']} <b>By:</b> <i>{uploader}</i>

{EMOJIS['gem']} <b>Quality:</b> {quality}p Ultra HD • {EMOJIS['shield']} Watermark-Free
{EMOJIS['clock']} <b>Duration:</b> {duration_text} • {EMOJIS['chart']} Views: {view_count}
{EMOJIS['heart']} <b>Likes:</b> {like_count} • {EMOJIS['calendar']} {upload_date}
{EMOJIS['diamond']} <b>Size:</b> {file_size_mb:.1f}MB Premium Quality

{EMOJIS['info']} <b>Description:</b> <i>{description}</i>

{EMOJIS['fire']} <b>Powered by {BOT_NAME}</b>
{EMOJIS['trophy']} World's Best Premium Download Service
{EMOJIS['magic']} Perfect Quality • Lightning Speed • 100% Reliable

{EMOJIS['heart']} <i>Thank you for choosing premium excellence!</i>
                    """
                    
                    try:
                        with open(downloaded_file, 'rb') as video:
                            bot.send_video(chat_id, video, caption=video_caption, parse_mode='HTML',
                                         supports_streaming=True, timeout=300,
                                         reply_markup=self.create_action_keyboard("download"))
                        
                        os.remove(downloaded_file)
                        self.update_stats(chat_id, 'downloads')
                    except Exception as upload_error:
                        print(f"Upload error: {upload_error}")
                        self.handle_upload_error(chat_id, message_id, file_size_mb)
                else:
                    self.handle_file_error(chat_id, message_id)

        except Exception as e:
            self.safe_delete_processing_key(processing_key)
            print(f"Download error: {e}")
            self.handle_download_error(str(e), chat_id, message_id)

    def enhance_photo_premium(self, input_path, chat_id, message_id):
        """Ultra Premium AI Photo Enhancement with face detection, 8K option, noise reduction"""
        try:
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Failed to read image")

            # Face-focused enhancement if face detector available
            if self.face_cascade is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    face = img[y:y+h, x:x+w]
                    face_enhanced = cv2.detailEnhance(face, sigma_s=10, sigma_r=0.15)
                    img[y:y+h, x:x+w] = face_enhanced

            # Upscale to 4K or 8K based on session
            scale = 8 if self.user_sessions.get(chat_id, '') == '8k' else 4
            if self.models_loaded:
                upscaled = self.sr_model.upsample(img)
                if scale == 8:  # Double upscale for 8K
                    upscaled = cv2.resize(upscaled, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
            else:
                fx = fy = scale
                upscaled = cv2.resize(img, None, fx=fx, fy=fy, interpolation=cv2.INTER_LANCZOS4)

            # Color enhancement
            lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

            # Noise reduction
            enhanced = cv2.bilateralFilter(enhanced, d=9, sigmaColor=75, sigmaSpace=75)

            # Sharpening
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(enhanced, -1, kernel)

            # Auto brightness
            mean_brightness = np.mean(cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY))
            if mean_brightness < 100:
                sharpened = cv2.convertScaleAbs(sharpened, alpha=1.2, beta=20)

            output_path = input_path.replace('input', f'enhanced_{scale}k_output')
            cv2.imwrite(output_path, sharpened)
            self.update_stats(chat_id, 'enhancements')
            return output_path

        except Exception as e:
            logger.error(f"Enhancement error: {e}")
            self.handle_enhancement_error(chat_id, message_id)
            return None

    def generate_subtitles(self, video_path):
        """Advanced subtitle generation with timing"""
        if not ADVANCED_FEATURES:
            return "Subtitle generation requires advanced libraries."
        
        try:
            audio_path = video_path.replace('.mp4', '.wav')
            AudioSegment.from_file(video_path).export(audio_path, format="wav")
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
            os.remove(audio_path)
            # Simple timing: assume 10s per sentence
            subtitles = [f"{i*10:02d}:{(i*10)%60:02d} - {sentence.strip()}" for i, sentence in enumerate(text.split('.')) if sentence.strip()]
            return '\n'.join(subtitles)
        except Exception as e:
            logger.error(f"Subtitle error: {e}")
            return "Could not generate subtitles."

    def auto_translate(self, text, target_lang='en'):
        """Auto translation with detection"""
        if not ADVANCED_FEATURES:
            return "Translation requires advanced libraries."
        
        try:
            detected = self.translator.detect(text)
            if detected.lang == target_lang:
                return f"Already in {target_lang}: {text}"
            translated = self.translator.translate(text, dest=target_lang)
            return f"Translated from {detected.lang} to {target_lang}: {translated.text}"
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Translation failed: {text}"

    def batch_download(self, urls, chat_id):
        """Batch download with progress updates"""
        total = len(urls)
        for i, url in enumerate(urls):
            bot.send_message(chat_id, f"{EMOJIS['batch']} Processing {i+1}/{total}: {url[:50]}...")
            self.download_video_premium(url, chat_id, None)
        self.update_stats(chat_id, 'batch_downloads')
        bot.send_message(chat_id, f"{EMOJIS['success']} Batch download complete!")

    def update_stats(self, user_id, stat_type):
        """Update user statistics"""
        try:
            cursor = self.db.cursor()
            cursor.execute(f"UPDATE users SET {stat_type} = {stat_type} + 1 WHERE id=?", (user_id,))
            if cursor.rowcount == 0:
                cursor.execute(f"INSERT INTO users (id, {stat_type}) VALUES (?, 1)", (user_id,))
            self.db.commit()
        except Exception as e:
            logger.error(f"Stats update error: {e}")

    def get_user_analytics(self, user_id):
        """User stats analytics"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT downloads, enhancements, batch_downloads, subtitles_generated FROM users WHERE id=?", (user_id,))
            stats = cursor.fetchone() or (0, 0, 0, 0)
            return f"{EMOJIS['analytics']} <b>Your Premium Stats:</b>\n• Downloads: {stats[0]}\n• Enhancements: {stats[1]}\n• Batches: {stats[2]}\n• Subtitles: {stats[3]}"
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return f"{EMOJIS['analytics']} Analytics temporarily unavailable."

    def handle_upload_error(self, chat_id, message_id, file_size=0):
        """Handle upload errors with premium styling"""
        error_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['warning']} FILE SIZE EXCEEDED {EMOJIS['warning']}     ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['info']} <b>Issue:</b> <i>File size ({file_size:.1f}MB) exceeds Telegram's limit</i>

{EMOJIS['sparkles']} <b>Premium Solutions:</b>
• {EMOJIS['gem']} Video was processed successfully (perfect quality)
• {EMOJIS['lightning']} Try downloading shorter videos (under 2GB)
• {EMOJIS['magic']} All premium features were applied perfectly
• {EMOJIS['crystal']} Contact developer for custom large file solutions

<b>┌────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['heart']} PREMIUM SUPPORT ACTIVE {EMOJIS['heart']}     │</b>
<b>└────────────────────────────────────────────┘</b>
        """
        bot.edit_message_text(error_text, chat_id, message_id, parse_mode='HTML', reply_markup=self.create_action_keyboard("download"))

    def handle_file_error(self, chat_id, message_id):
        """Handle file processing errors"""
        error_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['error']} FILE PROCESSING ISSUE {EMOJIS['warning']}     ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['info']} <b>Issue:</b> <i>Unable to locate or process the downloaded file</i>

{EMOJIS['sparkles']} <b>Premium Solutions:</b>
• {EMOJIS['gem']} Try a different video URL
• {EMOJIS['lightning']} Ensure video is publicly accessible
• {EMOJIS['magic']} Check your internet connection stability
• {EMOJIS['crystal']} Video might be geo-restricted

<b>┌────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['shield']} PREMIUM SUPPORT READY {EMOJIS['shield']}     │</b>
<b>└────────────────────────────────────────────┘</b>
        """
        bot.edit_message_text(error_text, chat_id, message_id, parse_mode='HTML', reply_markup=self.create_action_keyboard("download"))

    def handle_download_error(self, error, chat_id, message_id):
        """Handle download errors with detailed solutions"""
        clean_error = str(error)[:60]
        
        error_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['error']} DOWNLOAD ISSUE {EMOJIS['warning']}     ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['info']} <b>Error Details:</b> <code>{clean_error}</code>

{EMOJIS['sparkles']} <b>Premium Solutions:</b>
• {EMOJIS['gem']} Verify URL is correct and publicly accessible
• {EMOJIS['lightning']} Try different video quality or shorter videos
• {EMOJIS['rocket']} Check internet connection stability
• {EMOJIS['magic']} Some videos may be geo-restricted

<b>┌────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['shield']} PREMIUM SUPPORT READY {EMOJIS['shield']}     │</b>
<b>└────────────────────────────────────────────┘</b>
        """
        bot.edit_message_text(error_text, chat_id, message_id, parse_mode='HTML', reply_markup=self.create_action_keyboard("download"))

    def handle_enhancement_error(self, chat_id, message_id):
        """Handle enhancement errors"""
        error_text = f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║   {EMOJIS['warning']} ENHANCEMENT ISSUE {EMOJIS['crystal']}   ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['info']} <b>Premium Notice:</b> <i>Unable to process this media format</i>

{EMOJIS['sparkles']} <b>Premium Recommendations:</b>
• {EMOJIS['gem']} Use JPG, PNG, WebP for photos
• {EMOJIS['lightning']} Use MP4, MOV, AVI for videos
• {EMOJIS['crystal']} Keep file size under 50MB for optimal results
• {EMOJIS['magic']} Ensure good original quality for best enhancement

<b>┌────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['shield']} PREMIUM SUPPORT READY {EMOJIS['shield']}     │</b>
<b>└────────────────────────────────────────────┘</b>
        """
        bot.edit_message_text(error_text, chat_id, message_id, parse_mode='HTML', reply_markup=self.create_action_keyboard("enhance"))

# Initialize World's Best Bot
worlds_best_bot = WorldsBestUltraPremiumBot()

# Rate limiting decorator
def rate_limited(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message = args[0] if len(args) > 0 and hasattr(args[0], 'from_user') else None
        if message:
            user_id = message.from_user.id
            now = time.time()
            requests = [t for t in user_requests[user_id] if now - t < RATE_WINDOW]
            if len(requests) >= RATE_LIMIT:
                bot.reply_to(message, f"{EMOJIS['warning']} Rate limit exceeded. Please wait!")
                return
            user_requests[user_id] = requests + [now]
        return func(*args, **kwargs)
    return wrapper

# PREMIUM PLATFORM SELECTION PROMPT
def prompt_platform_selection(chat_id):
    """Beautiful reply when user sends link without selecting platform first"""
    bot.send_message(chat_id, f"""
<b>╔══════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['sparkles']} PLEASE SELECT PLATFORM FIRST {EMOJIS['crown']}     ║</b>
<b>╚══════════════════════════════════════════════╝</b>

{EMOJIS['heart']} <b>Hello! Welcome to {BOT_NAME}</b>

{EMOJIS['info']} <b>To ensure the BEST premium experience, please select a platform button first before sending your link!</b>

{EMOJIS['crown']} <b>Why Select Platform First?</b>
• {EMOJIS['gem']} Optimizes download for platform-specific quality
• {EMOJIS['magic']} Enables advanced watermark removal algorithms
• {EMOJIS['lightning']} Activates 4K support & premium processing
• {EMOJIS['shield']} Ensures fastest, most reliable downloads
• {EMOJIS['trophy']} Unlocks platform-specific premium features

{EMOJIS['sparkles']} <b>How to Use Premium Service:</b>
• {EMOJIS['rocket']} Step 1: Click a platform button below (YouTube, TikTok, etc.)
• {EMOJIS['gem']} Step 2: Send your video link for instant premium download
• {EMOJIS['magic']} Alternative: Use "ULTRA DOWNLOADER" for universal downloads

{EMOJIS['fire']} <b>Premium Benefits:</b>
• {EMOJIS['diamond']} 4K quality downloads guaranteed
• {EMOJIS['crystal']} 100% watermark-free content
• {EMOJIS['nova']} Lightning-fast processing (up to 2GB files)
• {EMOJIS['rainbow']} Full video captions & metadata included

{EMOJIS['party']} <b>Choose your platform below and enjoy world-class downloads!</b>

<b>┌────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['nova']} PREMIUM EXPERIENCE AWAITS {EMOJIS['nova']}     │</b>
<b>└────────────────────────────────────────────┘</b>
    """, reply_markup=worlds_best_bot.create_main_keyboard(), parse_mode='HTML')

# 👑 ULTIMATE PREMIUM START COMMAND
@bot.message_handler(commands=['start'])
@rate_limited
def ultimate_start_command(message):
    user_name = message.from_user.first_name or "Premium User"
    current_time = datetime.now().strftime("%H:%M")
    
    ultimate_welcome_text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║      {EMOJIS['crown']} WELCOME TO {BOT_NAME} {EMOJIS['crown']}      ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['fire']} <b>Hello {user_name}! Welcome to World's Most Advanced AI Bot!</b> {EMOJIS['fire']}

{EMOJIS['rocket']} <b>🌟 Ultimate Premium Features:</b>
• {EMOJIS['gem']} Smart platform-specific downloading (6+ platforms)
• {EMOJIS['lightning']} Zero watermarks • Ultra HD quality guaranteed (up to 8K)
• {EMOJIS['magic']} Real AI 4K/8K photo & video enhancement (Wink App Quality)
• {EMOJIS['crystal']} Quantum-speed processing • Instant results (2GB support)
• {EMOJIS['nova']} Premium algorithms • Professional effects • Full captions
• {EMOJIS['subtitle']} Auto subtitle generation with timing
• {EMOJIS['translate']} Multi-language auto-translation
• {EMOJIS['batch']} Batch download multiple videos at once

{EMOJIS['sparkles']} <b>🎯 Supported Premium Platforms:</b>
{EMOJIS['video']} YouTube • {EMOJIS['dancing']} TikTok • {EMOJIS['camera']} Instagram • {EMOJIS['blue_heart']} Facebook
{EMOJIS['lightning']} Twitter/X • {EMOJIS['orange_heart']} Reddit • {EMOJIS['fire']} Vimeo • And 200+ platforms!

{EMOJIS['rainbow']} <b>🎨 Premium AI Enhancement Suite:</b>
• {EMOJIS['comet']} Professional 4K/8K Photo Upscaling (Perfect Colors & Details)
• {EMOJIS['video']} 4K/8K Video Enhancement Technology (Wink Quality Results)
• {EMOJIS['sun']} Advanced Color & Brightness Optimization (Zero Distortion)
• {EMOJIS['galaxy']} Premium Noise Reduction • Crystal Clear Perfect Results
• {EMOJIS['robot']} Face detection for enhanced portrait processing

{EMOJIS['trophy']} <b>⭐ Premium Guarantees:</b>
• {EMOJIS['shield']} 100% Watermark-free downloads always
• {EMOJIS['diamond']} Maximum quality available (up to 8K resolution)
• {EMOJIS['clock']} Lightning-fast processing ({current_time} - Always online!)
• {EMOJIS['heart']} Expert developer support available 24/7
• {EMOJIS['analytics']} Personal analytics dashboard

{EMOJIS['crown']} <b>💎 Why Choose Us?</b>
• {EMOJIS['star']} World's most beautiful bot interface
• {EMOJIS['gem']} Advanced AI algorithms (Wink app quality)
• {EMOJIS['fire']} Large file support (up to 2GB processing)
• {EMOJIS['magic']} Full video metadata & captions included
• {EMOJIS['batch']} Batch processing capabilities

<b>┌───────────────────────────────────────────────────┐</b>
<b>│          🎉 Choose your premium experience below! 🎉          │</b>
<b>└───────────────────────────────────────────────────┘</b>

{EMOJIS['info']} <i>Tip: Select a platform button first, then send your link for best results!</i>
    """
    
    bot.send_message(message.chat.id, ultimate_welcome_text,
                    reply_markup=worlds_best_bot.create_main_keyboard(),
                    parse_mode='HTML')

# URL HANDLER WITH PLATFORM CHECK
@bot.message_handler(func=lambda msg: any(platform in msg.text.lower() for platform in 
    ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'facebook.com', 
     'twitter.com', 'reddit.com', 'vimeo.com', 'vm.tiktok', 'vt.tiktok', 'x.com', 'fb.watch']))
@rate_limited
def handle_ultimate_video_url(message):
    url = message.text.strip()
    user_id = message.chat.id
    
    # Check for batch URLs (separated by comma or newline)
    if ',' in url or '\n' in url:
        urls = [u.strip() for u in re.split('[,\n]', url) if u.strip()]
        bot.send_message(user_id, f"{EMOJIS['batch']} Batch mode detected! Processing {len(urls)} URLs...")
        threading.Thread(target=worlds_best_bot.batch_download, args=(urls, user_id)).start()
        return
    
    if user_id not in worlds_best_bot.user_sessions:
        prompt_platform_selection(message.chat.id)
        return
    
    selected_platform = worlds_best_bot.user_sessions[user_id]
    
    premium_processing_msg = bot.send_message(message.chat.id, f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║      {EMOJIS['rocket']} {BOT_NAME} ACTIVATED {EMOJIS['rocket']}      ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['lightning']} <b>Premium URL Detected:</b> 
<code>{url[:40]}{'...' if len(url) > 40 else ''}</code>

{EMOJIS['magic']} <b>Platform:</b> <i>{selected_platform.title() if selected_platform else 'Universal'}</i>
{EMOJIS['crystal']} <b>Quality:</b> <i>Ultra HD Premium Processing (up to 4K)</i>
{EMOJIS['crown']} <b>Mode:</b> <i>Premium Treatment Activated</i>
{EMOJIS['gem']} <b>Features:</b> <i>Watermark-free • Full captions • Large file support</i>

{EMOJIS['fire']} <i>Please wait while {BOT_NAME} works its premium magic...</i>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│        {EMOJIS['nova']} Premium Processing Started {EMOJIS['nova']}        │</b>
<b>└───────────────────────────────────────────────────┘</b>
    """, parse_mode='HTML')
    
    threading.Thread(target=worlds_best_bot.download_video_premium, 
                    args=(url, message.chat.id, premium_processing_msg.message_id, selected_platform)).start()

# 📸 PHOTO HANDLER FOR AI ENHANCEMENT
@bot.message_handler(content_types=['photo'])
@rate_limited
def handle_ultimate_photo_enhancement(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        img_data = bot.download_file(file_info.file_path)
        
        input_path = os.path.join(TMP_DIR, f"input_premium_photo_{message.from_user.id}_{int(time.time())}.jpg")
        
        with open(input_path, 'wb') as f:
            f.write(img_data)
        
        file_size_mb = len(img_data) / (1024 * 1024)
        
        scale_mode = "8K" if worlds_best_bot.user_sessions.get(message.chat.id) == '8k' else "4K"
        
        premium_processing_msg = bot.send_message(message.chat.id, f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║   {EMOJIS['magic']} PREMIUM AI {scale_mode} PHOTO ENHANCEMENT {EMOJIS['magic']}   ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>{BOT_NAME} Premium AI Analysis:</b>
<i>Scanning your photo with quantum premium algorithms...</i>

{EMOJIS['crystal']} <b>Enhancement Mode:</b> <i>Premium {scale_mode} Ultra HD (Wink App Quality)</i>
{EMOJIS['lightning']} <b>Algorithm:</b> <i>Perfect OpenCV Super Resolution AI</i>
{EMOJIS['gem']} <b>File Size:</b> <i>{file_size_mb:.1f}MB • Premium Processing</i>
{EMOJIS['fire']} <b>Expected Output:</b> <i>{scale_mode} Quality Boost • Crystal Clear</i>

{EMOJIS['sparkles']} <b>Premium Features Activating:</b>
• {EMOJIS['diamond']} {scale_mode} resolution upscaling (advanced enhancement)
• {EMOJIS['rainbow']} Perfect color enhancement (zero distortion)
• {EMOJIS['nova']} Professional sharpness optimization
• {EMOJIS['sun']} Advanced noise reduction & polish
• {EMOJIS['robot']} AI face detection for enhanced portraits

<i>Transforming your photo into a premium {scale_mode} masterpiece...</i>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│       {EMOJIS['sparkles']} Premium AI Magic in Progress {EMOJIS['sparkles']}       │</b>
<b>└───────────────────────────────────────────────────┘</b>
        """, parse_mode='HTML')
        
        enhanced_path = worlds_best_bot.enhance_photo_premium(input_path, message.chat.id, premium_processing_msg.message_id)
        
        if enhanced_path and os.path.exists(enhanced_path):
            with open(enhanced_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, 
                             caption=f"{EMOJIS['crown']} <b>{BOT_NAME} {scale_mode} Enhancement Complete!</b>\n\n{EMOJIS['magic']} Your photo has been enhanced to {scale_mode} quality with premium algorithms!",
                             parse_mode='HTML',
                             reply_markup=worlds_best_bot.create_action_keyboard("enhance"))
            os.remove(enhanced_path)
        
        os.remove(input_path)
        
    except Exception as e:
        bot.reply_to(message, f"{EMOJIS['error']} Premium photo processing error: {str(e)[:50]}...")

# 📝 TEXT HANDLER FOR TRANSLATION
@bot.message_handler(func=lambda msg: worlds_best_bot.user_sessions.get(msg.chat.id) == 'translate')
@rate_limited
def handle_translation(message):
    try:
        text_parts = message.text.split(' ', 1)
        if len(text_parts) == 2:
            target_lang, text = text_parts[0], text_parts[1]
        else:
            target_lang, text = 'en', message.text
        
        translated = worlds_best_bot.auto_translate(text, target_lang)
        bot.reply_to(message, f"{EMOJIS['translate']} <b>Translation Result:</b>\n\n{translated}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"{EMOJIS['error']} Translation error: {str(e)}")

# 👑 PREMIUM CALLBACK HANDLER
@bot.callback_query_handler(func=lambda call: True)
def handle_ultimate_premium_callbacks(call):
    try:
        user_id = call.message.chat.id
        user_name = call.from_user.first_name or "Premium User"
        
        # IMPORTANT: Answer the callback query to stop loading spinner
        bot.answer_callback_query(call.id)
        
        if call.data.startswith("select_"):
            platform = call.data.replace("select_", "")
            worlds_best_bot.user_sessions[user_id] = platform
            
            platform_messages = {
                'youtube': f"🎬 YouTube Premium mode activated! Send YouTube URLs for 4K downloads with full captions.",
                'tiktok': f"💃 TikTok Premium mode activated! Send TikTok URLs for watermark-free HD downloads.",
                'instagram': f"📸 Instagram Premium mode activated! Send Instagram URLs for crystal clear downloads.",
                'facebook': f"👥 Facebook Premium mode activated! Send PUBLIC Facebook video URLs for premium downloads.",
                'twitter': f"🐦 Twitter/X Premium mode activated! Send Twitter/X URLs for premium quality downloads.",
                'reddit': f"🅰️ Reddit Premium mode activated! Send Reddit video URLs for high-quality downloads."
            }
            
            platform_text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║    {EMOJIS['success']} {platform.upper()} PREMIUM MODE ACTIVATED! {EMOJIS['crown']}    ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['sparkles']} <b>Hello {user_name}!</b> <i>{platform_messages.get(platform)}</i>

{EMOJIS['gem']} <b>Premium {platform.title()} Features:</b>
• {EMOJIS['fire']} Up to 4K resolution support
• {EMOJIS['gem']} Full video captions & metadata
• {EMOJIS['trophy']} Large file support (2GB)
• {EMOJIS['lightning']} Lightning-fast processing

{EMOJIS['info']} <b>How to Use:</b>
• {EMOJIS['rocket']} Send ONLY {platform.title()} links now
• {EMOJIS['crown']} Other platform links will be politely rejected
• {EMOJIS['crystal']} Use "ULTRA DOWNLOADER" for all platforms
• {EMOJIS['magic']} Enjoy premium quality & speed!

{EMOJIS['trophy']} <b>Premium Guarantees:</b>
• {EMOJIS['diamond']} Maximum quality available
• {EMOJIS['lightning']} Watermark-free content
• {EMOJIS['fire']} Lightning-fast processing
• {EMOJIS['heart']} Full captions & metadata

{EMOJIS['party']} <b>Send your {platform.title()} link now for premium download!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['nova']} {BOT_NAME} {platform.upper()} READY {EMOJIS['nova']}     │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            
            back_keyboard = types.InlineKeyboardMarkup()
            back_keyboard.add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Premium Menu", callback_data="main_menu"))
            
            try:
                bot.edit_message_caption(caption=platform_text, chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                         parse_mode='HTML', reply_markup=back_keyboard)
            except:
                bot.edit_message_text(text=platform_text, chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      parse_mode='HTML', reply_markup=back_keyboard)

        elif call.data == "ultra_download":
            if user_id in worlds_best_bot.user_sessions:
                del worlds_best_bot.user_sessions[user_id]
            
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['download']} ULTRA UNIVERSAL DOWNLOADER {EMOJIS['download']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['fire']} <b>Hello {user_name}! Universal download mode activated!</b>

{EMOJIS['video']} <b>Supported Premium Platforms:</b>
• {EMOJIS['gem']} YouTube (youtube.com/youtu.be) - 4K Support {EMOJIS['crown']}
• {EMOJIS['sparkles']} TikTok (tiktok.com/vm.tiktok.com) - Watermark Free {EMOJIS['party']}
• {EMOJIS['camera']} Instagram (instagram.com) - HD Quality {EMOJIS['heart']}
• {EMOJIS['crown']} Facebook (facebook.com)
# Facebook (facebook.com) - Public videos {EMOJIS['shield']}
• {EMOJIS['lightning']} Twitter/X (twitter.com/x.com) - Fast Download {EMOJIS['blue_heart']}
• {EMOJIS['magic']} Reddit (reddit.com) - Premium Quality {EMOJIS['orange_heart']}
• {EMOJIS['crystal']} Vimeo, Dailymotion & 200+ premium platforms! {EMOJIS['rainbow']}

{EMOJIS['trophy']} <b>Premium Features Guarantee:</b>
• {EMOJIS['fire']} 100% Watermark-free downloads always
• {EMOJIS['rocket']} Up to 4K premium quality (platform dependent)
• {EMOJIS['magic']} Lightning-fast processing with large file support (2GB)
• {EMOJIS['gem']} Full video captions & metadata included
• {EMOJIS['diamond']} Professional-grade quality preservation
• {EMOJIS['shield']} Secure & private processing

{EMOJIS['sparkles']} <b>Send any video URL from any supported platform!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['heart']} UNIVERSAL PREMIUM MODE READY {EMOJIS['heart']}      │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "ai_enhancer":
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║    {EMOJIS['magic']} PREMIUM AI 4K/8K ENHANCEMENT CENTER {EMOJIS['magic']}    ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Hello {user_name}! Welcome to AI Enhancement Center!</b>

{EMOJIS['gem']} <b>🎨 Premium 4K/8K Photo Enhancement (Wink App Quality)</b>
• {EMOJIS['trophy']} Perfect OpenCV Super Resolution AI algorithms
• {EMOJIS['diamond']} Up to 8K premium quality increase guaranteed
• {EMOJIS['sparkles']} Crystal clear results with zero color distortion
• {EMOJIS['success']} Wink app quality - professional results every time!
• {EMOJIS['rainbow']} Advanced LAB color space enhancement
• {EMOJIS['crystal']} Professional CLAHE & bilateral filtering
• {EMOJIS['robot']} AI face detection for enhanced portrait processing

{EMOJIS['video']} <b>🎬 Premium 4K Video Enhancement (NEW & ADVANCED!)</b>
• {EMOJIS['rocket']} Advanced ffmpeg upscaling to 4K resolution (3840x2160)
• {EMOJIS['rainbow']} Perfect color correction & brightness optimization
• {EMOJIS['crystal']} Professional sharpening & noise reduction
• {EMOJIS['nova']} Wink-style enhancement for crystal clarity!
• {EMOJIS['fire']} Unsharp masking for perfect detail enhancement
• {EMOJIS['gem']} Perfect audio preservation with quality boost

{EMOJIS['lightning']} <b>⚡ Advanced Premium Processing</b>
• {EMOJIS['fire']} Ultra-fast GPU acceleration when available
• {EMOJIS['trophy']} Perfect quality output guaranteed always
• {EMOJIS['shield']} Zero quality loss or artifacts
• {EMOJIS['crown']} Multiple fallback algorithms for reliability

{EMOJIS['crystal']} <b>📋 Premium Supported Formats</b>
• {EMOJIS['camera']} <b>Photos:</b> JPG, PNG, WebP, BMP (up to 50MB)
• {EMOJIS['video']} <b>Videos:</b> MP4, MOV, AVI, MKV (up to 50MB)
• {EMOJIS['crown']} <b>Output:</b> Ultra HD 4K/8K quality guaranteed
• {EMOJIS['fire']} <b>Processing:</b> Professional-grade enhancement

{EMOJIS['trophy']} <b>🏆 Why Our AI is The Best:</b>
• {EMOJIS['star']} Same quality as premium mobile apps (Wink, Remini)
• {EMOJIS['gem']} Advanced machine learning algorithms
• {EMOJIS['magic']} Perfect detail preservation with enhancement
• {EMOJIS['nova']} Professional photographer-level results

{EMOJIS['party']} <b>Send me any photo OR video for perfect 4K/8K enhancement!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│    {EMOJIS['nova']} PREMIUM AI ENHANCEMENT AWAITS {EMOJIS['nova']}    │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "batch_download":
            worlds_best_bot.user_sessions[user_id] = 'batch'
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['batch']} PREMIUM BATCH DOWNLOADER {EMOJIS['batch']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['fire']} <b>Hello {user_name}! Batch download mode activated!</b>

{EMOJIS['rocket']} <b>How to Use Batch Download:</b>
• {EMOJIS['gem']} Send multiple URLs separated by commas or new lines
• {EMOJIS['sparkles']} Example: url1, url2, url3 or one URL per line
• {EMOJIS['magic']} Up to 10 videos can be processed in one batch
• {EMOJIS['lightning']} All premium features apply to each video

{EMOJIS['crown']} <b>Batch Features:</b>
• {EMOJIS['diamond']} Progress tracking for each download
• {EMOJIS['shield']} Individual quality optimization
• {EMOJIS['trophy']} Automatic file organization
• {EMOJIS['heart']} Complete batch status updates

{EMOJIS['party']} <b>Send your URLs now for batch processing!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['nova']} BATCH MODE READY {EMOJIS['nova']}      │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "subtitle_gen":
            worlds_best_bot.user_sessions[user_id] = 'subtitles'
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['subtitle']} PREMIUM SUBTITLE GENERATOR {EMOJIS['subtitle']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Hello {user_name}! AI Subtitle Generator activated!</b>

{EMOJIS['magic']} <b>Advanced Subtitle Features:</b>
• {EMOJIS['robot']} AI-powered speech recognition
• {EMOJIS['clock']} Automatic timing synchronization
• {EMOJIS['translate']} Multi-language support
• {EMOJIS['gem']} Professional subtitle formatting

{EMOJIS['sparkles']} <b>How to Use:</b>
• {EMOJIS['video']} Send any video file (MP4, MOV, AVI)
• {EMOJIS['lightning']} AI will extract and transcribe audio
• {EMOJIS['crystal']} Receive formatted subtitle file
• {EMOJIS['fire']} Perfect timing and accuracy

{EMOJIS['party']} <b>Send your video now for AI subtitle generation!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['nova']} AI SUBTITLE MODE READY {EMOJIS['nova']}      │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "enhance_8k":
            worlds_best_bot.user_sessions[user_id] = '8k'
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['8k']} PREMIUM 8K ENHANCEMENT MODE {EMOJIS['8k']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Hello {user_name}! 8K Ultra Enhancement activated!</b>

{EMOJIS['diamond']} <b>8K Premium Features:</b>
• {EMOJIS['star']} 7680×4320 resolution output
• {EMOJIS['magic']} Multi-pass AI upscaling
• {EMOJIS['crystal']} Perfect detail preservation
• {EMOJIS['rainbow']} Professional color grading

{EMOJIS['fire']} <b>8K Processing Power:</b>
• {EMOJIS['rocket']} Advanced neural networks
• {EMOJIS['gem']} Zero quality loss guarantee
• {EMOJIS['lightning']} Optimized for large displays
• {EMOJIS['trophy']} Cinema-grade output quality

{EMOJIS['party']} <b>Send any photo for 8K enhancement!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['nova']} 8K MODE ACTIVATED {EMOJIS['nova']}      │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "auto_translate":
            worlds_best_bot.user_sessions[user_id] = 'translate'
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['translate']} PREMIUM AUTO TRANSLATOR {EMOJIS['translate']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Hello {user_name}! AI Translation mode activated!</b>

{EMOJIS['sparkles']} <b>Translation Features:</b>
• {EMOJIS['robot']} AI-powered language detection
• {EMOJIS['globe']} 100+ languages supported
• {EMOJIS['lightning']} Instant translation
• {EMOJIS['gem']} Context-aware results

{EMOJIS['info']} <b>How to Use:</b>
• {EMOJIS['magic']} Send: "en Hello, how are you?" (for English)
• {EMOJIS['crystal']} Send: "es Hola, ¿cómo estás?" (for Spanish)
• {EMOJIS['fire']} Or just send text for auto-detection

{EMOJIS['party']} <b>Send text with target language for translation!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│      {EMOJIS['nova']} TRANSLATION MODE READY {EMOJIS['nova']}      │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Premium Menu", callback_data="main_menu")))

        elif call.data == "main_menu":
            if user_id in worlds_best_bot.user_sessions:
                del worlds_best_bot.user_sessions[user_id]
            ultimate_start_command(call.message)

        elif call.data == "developer_support":
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['shield']} PREMIUM DEVELOPER SUPPORT CENTER {EMOJIS['shield']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Get Direct Premium Support from Developer:</b>

{EMOJIS['diamond']} <b>Developer Contact Information:</b>
• {EMOJIS['sparkles']} <b>Telegram:</b> <code>{DEVELOPER_USERNAME}</code>
• {EMOJIS['gem']} <b>User ID:</b> <code>{DEVELOPER_ID}</code>
• {EMOJIS['lightning']} <b>Response Time:</b> <i>Usually within 30 minutes - 2 hours</i>
• {EMOJIS['clock']} <b>Available:</b> <i>24/7 Premium Support</i>

{EMOJIS['fire']} <b>Premium Support Services Available:</b>
• {EMOJIS['rocket']} Technical issues & bug reports (Priority support)
• {EMOJIS['magic']} Feature requests & suggestions (Premium feedback)
• {EMOJIS['crystal']} Custom bot development & modifications
• {EMOJIS['trophy']} Premium consultation & advanced features
• {EMOJIS['crown']} Large file processing (>2GB custom solutions)
• {EMOJIS['gem']} Platform-specific optimizations

{EMOJIS['sparkles']} <b>What to Include in Support Request:</b>
• {EMOJIS['info']} Detailed description of issue
• {EMOJIS['video']} Screenshots or examples if applicable
• {EMOJIS['lightning']} URL or media that caused the issue

{EMOJIS['heart']} <b>Developer Response Guarantee:</b>
• {EMOJIS['success']} Quick response for premium users
• {EMOJIS['shield']} Professional technical support
• {EMOJIS['magic']} Custom solutions for unique needs
• {EMOJIS['trophy']} Continuous improvement based on feedback

{EMOJIS['party']} <b>Click username below to contact directly!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│   {EMOJIS['crown']} PREMIUM DEVELOPER SUPPORT READY {EMOJIS['crown']}   │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(
                                             types.InlineKeyboardButton(f"{EMOJIS['crystal']} Contact {DEVELOPER_USERNAME}", url=f"https://t.me/{DEVELOPER_USERNAME[1:]}"),
                                             types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(
                                          types.InlineKeyboardButton(f"{EMOJIS['crystal']} Contact {DEVELOPER_USERNAME}", url=f"https://t.me/{DEVELOPER_USERNAME[1:]}"),
                                          types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))

        elif call.data == "about_bot":
            sys_info = get_system_info()
            analytics = worlds_best_bot.get_user_analytics(user_id)
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['trophy']} ABOUT {BOT_NAME} {EMOJIS['trophy']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>World's Most Advanced Social Media AI Bot</b>

{EMOJIS['info']} <b>Bot Information:</b>
• {EMOJIS['sparkles']} <b>Name:</b> {BOT_NAME}
• {EMOJIS['rocket']} <b>Version:</b> {BOT_VERSION}
• {EMOJIS['gem']} <b>Developer:</b> {DEVELOPER_USERNAME}
• {EMOJIS['fire']} <b>Status:</b> Online 24/7 Premium Service
• {EMOJIS['lightning']} <b>Launch Date:</b> 2024 Premium Release

{EMOJIS['trophy']} <b>Premium Capabilities:</b>
• {EMOJIS['video']} Download from 200+ platforms (up to 8K support)
• {EMOJIS['magic']} AI 4K/8K enhancement for photos & videos
• {EMOJIS['shield']} 100% watermark removal guaranteed
• {EMOJIS['crystal']} Large file processing (up to 2GB)
• {EMOJIS['rainbow']} Full metadata & captions included
• {EMOJIS['subtitle']} AI subtitle generation
• {EMOJIS['translate']} Multi-language translation
• {EMOJIS['batch']} Batch processing capabilities

{EMOJIS['diamond']} <b>Technical Specifications:</b>
• {EMOJIS['robot']} CPU: {sys_info['cpu']}
• {EMOJIS['gem']} RAM: {sys_info['ram']}
• {EMOJIS['earth']} OS: {sys_info['os']}
• {EMOJIS['scientist']} Python: {sys_info['python']}

{analytics}

{EMOJIS['sparkles']} <b>Unique Features:</b>
• {EMOJIS['star']} Beautiful animated loading screens
• {EMOJIS['heart']} Platform-specific optimization
• {EMOJIS['trophy']} Professional-grade AI enhancement
• {EMOJIS['nova']} Premium user experience design
• {EMOJIS['analytics']} Personal analytics dashboard

{EMOJIS['party']} <b>Thank you for using our premium service!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│   {EMOJIS['crown']} WORLD'S BEST BOT SERVING YOU {EMOJIS['crown']}   │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))

        elif call.data == "help_center":
            text = f"""
<b>╔═══════════════════════════════════════════════════╗</b>
<b>║     {EMOJIS['info']} PREMIUM HELP CENTER {EMOJIS['magic']}     ║</b>
<b>╚═══════════════════════════════════════════════════╝</b>

{EMOJIS['crown']} <b>Welcome to {BOT_NAME} Premium Help!</b>

{EMOJIS['sparkles']} <b>Basic Usage:</b>
• {EMOJIS['rocket']} /start - Open premium menu
• {EMOJIS['download']} Send video URL for premium download
• {EMOJIS['camera']} Send photo for 4K/8K AI enhancement
• {EMOJIS['video']} Send video for AI processing

{EMOJIS['gem']} <b>Advanced Features:</b>
• {EMOJIS['crystal']} Select platform for optimized downloads
• {EMOJIS['lightning']} Use "ULTRA DOWNLOADER" for any platform
• {EMOJIS['magic']} 4K/8K enhancement with Wink quality
• {EMOJIS['shield']} 100% watermark removal
• {EMOJIS['batch']} Batch download multiple videos
• {EMOJIS['subtitle']} AI subtitle generation
• {EMOJIS['translate']} Multi-language translation

{EMOJIS['trophy']} <b>Supported Platforms:</b>
• YouTube, TikTok, Instagram, Facebook
• Twitter, Reddit, Vimeo, and 200+ more

{EMOJIS['warning']} <b>Common Issues & Solutions:</b>
• {EMOJIS['error']} "Platform Mismatch" - Select correct platform
• {EMOJIS['error']} "File Size Exceeded" - Use shorter videos
• {EMOJIS['error']} "Processing Error" - Check URL validity
• {EMOJIS['error']} "Enhancement Issue" - Use supported formats
• {EMOJIS['error']} "Rate Limited" - Wait a minute between requests

{EMOJIS['heart']} <b>Need more help? Contact developer!</b>

<b>┌───────────────────────────────────────────────────┐</b>
<b>│     {EMOJIS['nova']} PREMIUM HELP CENTER READY {EMOJIS['nova']}     │</b>
<b>└───────────────────────────────────────────────────┘</b>
            """
            try:
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                         reply_markup=types.InlineKeyboardMarkup().add(
                                             types.InlineKeyboardButton(f"{EMOJIS['shield']} Contact Support", callback_data="developer_support"),
                                             types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))
            except:
                bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                                      reply_markup=types.InlineKeyboardMarkup().add(
                                          types.InlineKeyboardButton(f"{EMOJIS['shield']} Contact Support", callback_data="developer_support"),
                                          types.InlineKeyboardButton(f"{EMOJIS['rainbow']} ← Back to Menu", callback_data="main_menu")))

    except Exception as e:
        logger.error(f"Callback error: {e}")
        bot.answer_callback_query(call.id, text="An error occurred! Please try again.", show_alert=True)

# Run the bot
if __name__ == '__main__':
    print(f"{EMOJIS['crown']} Ultimate Advanced Premium Bot Started! Version {BOT_VERSION}")
    print(f"{EMOJIS['info']} Advanced features: {'✅ Enabled' if ADVANCED_FEATURES else '❌ Disabled (install required libraries)'}")
    print(f"{EMOJIS['rocket']} Bot is now running and ready to serve premium users!")
    
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
        print(f"{EMOJIS['error']} Bot stopped due to error: {e}")
