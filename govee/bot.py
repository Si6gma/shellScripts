import discord
from discord.ext import commands
import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token and API key from environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GOVEE_API_KEY = os.getenv('GOVEE_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Govee device information (replace with your actual device details)
DEVICE_MACS = {
    'Desk Light': '0F:3F:D0:C9:07:30:0D:18',
    'Lamp 1': '63:53:D0:C9:07:3B:30:B2',
    'Lamp 2': '55:8D:D0:C9:07:39:1A:D0',
    'All': 'All'
}
DEVICE_MODEL = 'H6008'  # Replace with your device model, e.g., 'H6182'

# Map of color names to RGB values
COLOR_MAP = {
    'red': {'r': 255, 'g': 0, 'b': 0},
    'green': {'r': 0, 'g': 255, 'b': 0},
    'blue': {'r': 0, 'g': 0, 'b': 255},
    'yellow': {'r': 255, 'g': 255, 'b': 0},
    'purple': {'r': 128, 'g': 0, 'b': 128},
    'cyan': {'r': 0, 'g': 255, 'b': 255},
    'white': {'r': 255, 'g': 255, 'b': 255},
}

intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance with commands and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to send a command to the Govee API
async def send_govee_command(session, mac_address, model, command):
    headers = {
        'Govee-API-Key': GOVEE_API_KEY,
        'Content-Type': 'application/json',
    }
    url = 'https://developer-api.govee.com/v1/devices/control'
    body = {
        'device': mac_address,
        'model': model,
        'cmd': command
    }
    
    for attempt in range(3):  # Retry up to 3 times in case of failure
        try:
            async with session.put(url, headers=headers, json=body) as response:
                if response.status == 200:
                    logging.info(f"Command {command['name']} for device {mac_address} succeeded")
                    return True
                else:
                    logging.warning(f"Failed to send command {command['name']} to {mac_address}: {response.status} - {await response.text()}")
        except aiohttp.ClientError as e:
            logging.error(f"Client error while sending command {command['name']} to {mac_address}: {e}")
        await asyncio.sleep(1)  # Wait a bit before retrying

    return False

# Function to change Govee light color
async def set_light_color(mac_address, model, color):
    async with aiohttp.ClientSession() as session:
        return await send_govee_command(session, mac_address, model, {'name': 'color', 'value': color})

# Function to turn Govee light on or off
async def set_light_power(mac_address, model, power_state):
    async with aiohttp.ClientSession() as session:
        return await send_govee_command(session, mac_address, model, {'name': 'turn', 'value': power_state})

# Function to handle multiple device commands concurrently
async def set_all_lights_power(state):
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_govee_command(session, mac, DEVICE_MODEL, {'name': 'turn', 'value': state})
            for mac in DEVICE_MACS.values() if mac != 'All'
        ]
        results = await asyncio.gather(*tasks)
        return all(results)

async def set_all_lights_color(color):
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_govee_command(session, mac, DEVICE_MODEL, {'name': 'color', 'value': COLOR_MAP[color]})
            for mac in DEVICE_MACS.values() if mac != 'All'
        ]
        results = await asyncio.gather(*tasks)
        return all(results)

class DeviceSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Desk Light', style=discord.ButtonStyle.primary)
    async def desk_light_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Select an action for Desk Light:', view=LightControlView('Desk Light'), ephemeral=True)

    @discord.ui.button(label='Lamp 1', style=discord.ButtonStyle.primary)
    async def lamp1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Select an action for Lamp 1:', view=LightControlView('Lamp 1'), ephemeral=True)

    @discord.ui.button(label='Lamp 2', style=discord.ButtonStyle.primary)
    async def lamp2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Select an action for Lamp 2:', view=LightControlView('Lamp 2'), ephemeral=True)

    @discord.ui.button(label='All', style=discord.ButtonStyle.danger)
    async def all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Select an action for all devices:', view=LightControlView('All'), ephemeral=True)

class LightControlView(discord.ui.View):
    def __init__(self, device):
        super().__init__()
        self.device = device

    @discord.ui.button(label='Turn On', style=discord.ButtonStyle.success)
    async def turn_on_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.device == 'All':
            success = await set_all_lights_power('on')
            message = 'All lights turned on!' if success else 'Failed to turn on all lights.'
            await interaction.response.send_message(message)
        else:
            mac = DEVICE_MACS[self.device]
            success = await set_light_power(mac, DEVICE_MODEL, 'on')
            message = f'{self.device} turned on!' if success else f'Failed to turn on {self.device}.'
            await interaction.response.send_message(message)

    @discord.ui.button(label='Turn Off', style=discord.ButtonStyle.danger)
    async def turn_off_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.device == 'All':
            success = await set_all_lights_power('off')
            message = 'All lights turned off!' if success else 'Failed to turn off all lights.'
            await interaction.response.send_message(message)
        else:
            mac = DEVICE_MACS[self.device]
            success = await set_light_power(mac, DEVICE_MODEL, 'off')
            message = f'{self.device} turned off!' if success else f'Failed to turn off {self.device}.'
            await interaction.response.send_message(message)

    @discord.ui.button(label='Colors', style=discord.ButtonStyle.primary)
    async def color_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'Select a color for {self.device}:', view=ColorSelectView(self.device), ephemeral=True)

class ColorSelectView(discord.ui.View):
    def __init__(self, device):
        super().__init__()
        self.device = device

    async def color_callback(self, interaction: discord.Interaction, color_name):
        if self.device == 'All':
            success = await set_all_lights_color(color_name)
            message = f'All lights changed to {color_name}!' if success else f'Failed to change all lights to {color_name}.'
            await interaction.response.send_message(message)
        else:
            mac = DEVICE_MACS[self.device]
            success = await set_light_color(mac, DEVICE_MODEL, COLOR_MAP[color_name])
            message = f'{self.device} changed to {color_name}!' if success else f'Failed to change {self.device} to {color_name}.'
            await interaction.response.send_message(message)

    @discord.ui.button(label='Red', style=discord.ButtonStyle.secondary)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.color_callback(interaction, 'red')

    @discord.ui.button(label='Green', style=discord.ButtonStyle.secondary)
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.color_callback(interaction, 'green')

    @discord.ui.button(label='Blue', style=discord.ButtonStyle.secondary)
    async def blue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.color_callback(interaction, 'blue')

    # Add more color buttons as needed

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')

@bot.command(name='lights')
async def lights(ctx):
    await ctx.send('Select a device to control:', view=DeviceSelectView())

bot.run(DISCORD_BOT_TOKEN)
