from PIL import Image, ImageDraw, ImageFont
from web3 import Web3
from web3.middleware import geth_poa_middleware

# --- 1. Membuat Frame Airdrop ---

# Ukuran gambar frame
width, height = 800, 600
bg_color = (255, 255, 255)  # Warna latar belakang putih
frame_color = (0, 0, 255)  # Warna frame biru
text_color = (255, 255, 255)  # Warna teks putih

# Membuat gambar kosong dengan ukuran yang ditentukan
img = Image.new('RGB', (width, height), bg_color)

# Membuat objek drawing
draw = ImageDraw.Draw(img)

# Membuat frame (garis tepi)
frame_thickness = 20
draw.rectangle([frame_thickness, frame_thickness, width-frame_thickness, height-frame_thickness], outline=frame_color, width=frame_thickness)

# Menambahkan teks pada gambar
text = "Claim Airdrop!"
font = ImageFont.load_default()  # Anda bisa mengganti font jika perlu
text_width, text_height = draw.textsize(text, font=font)
text_position = ((width - text_width) // 2, (height - text_height) // 2)
draw.text(text_position, text, fill=text_color, font=font)

# Menambahkan gambar logo token
try:
    token_image = Image.open("token.png")  # Gambar token yang ingin ditambahkan
    token_width, token_height = token_image.size
    
    # Mengubah ukuran logo token agar pas dalam frame
    token_size = (100, 100)  # Ukuran baru untuk token
    token_image = token_image.resize(token_size)

    # Posisi gambar token di dalam frame
    token_position = ((width - token_size[0]) // 2, height - token_size[1] - 30)  # Menempatkan logo di bawah teks
    img.paste(token_image, token_position, token_image)  # Tempelkan gambar token

except FileNotFoundError:
    print("Gambar token tidak ditemukan. Pastikan 'token.png' ada di folder yang sama.")

# Simpan gambar ke file
img.save('airdrop_with_token.png')

# Tampilkan gambar
img.show()

# --- 2. Mengirim Token ERC-20 ---

# Koneksi ke node Ethereum (misalnya menggunakan Infura atau node lokal)
infura_url = "https://base-mainnet.infura.io"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Jika Anda menggunakan jaringan dengan Proof of Authority (seperti Rinkeby), aktifkan middleware POA
web3.middleware_stack.inject(geth_poa_middleware, layer=0)

# Pastikan terhubung ke Ethereum
if web3.isConnected():
    print("Terhubung ke Ethereum Network")

# Informasi wallet pengirim
sender_address = "0xE86AcB35d4fC679dD5AAFd7e8E026859acdc08f0"  # Ganti dengan alamat pengirim
private_key = "baff94f87e0161c4a331f6884e998ae64c0872b22f494c6e0177bdde76acde82"  # Ganti dengan private key pengirim (Hati-hati, jangan bagikan private key Anda!)

# Informasi token ERC-20
token_address = "0xBa09e8F1B61C307222d48DA85Ae9EF83c0aA5164"  # Ganti dengan alamat kontrak token ERC-20
token_abi = [
    # Bagian ABI untuk fungsi transfer dari kontrak token ERC-20
    {
        "constant": False,
        "inputs": [
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Membuat instance kontrak token
token_contract = web3.eth.contract(address=token_address, abi=token_abi)

# Alamat penerima dan jumlah token yang ingin dikirim
recipient_address = "0xRecipientAddress"  # Ganti dengan alamat penerima
amount = 1000 * 10**18  # Jumlah token yang akan dikirim (disesuaikan dengan desimal token, misalnya 18 desimal)

# Menyiapkan transaksi
nonce = web3.eth.getTransactionCount(sender_address)
gas_price = web3.eth.gas_price  # Gas price saat ini
gas_limit = 100000  # Estimasi gas limit

transaction = token_contract.functions.transfer(recipient_address, amount).buildTransaction({
    'chainId': 1,  # Mainnet Ethereum
    'gas': gas_limit,
    'gasPrice': gas_price,
    'nonce': nonce,
})

# Menandatangani transaksi
signed_transaction = web3.eth.account.signTransaction(transaction, private_key)

# Mengirim transaksi
transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
print(f"Transaksi berhasil dikirim! Hash transaksi: {web3.toHex(transaction_hash)}")
