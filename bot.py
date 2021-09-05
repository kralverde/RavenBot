# bot.py
import os
import json
import time

import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CONFIG = os.getenv('CONFIG')

class JSONConfig(dict):

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    def __init__(self, *args):
        dict.__init__(self, *args)

    def save_config(self):
        with open(CONFIG, 'w') as f:
            json.dump(self, f, cls=self.SetEncoder)

    def get(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        self.save_config()

try:
    with open(CONFIG, 'r') as f:
        config = JSONConfig(json.load(f))
except:
    config = JSONConfig()

if 'whitelist' in config:
    config['whitelist'] = set(config['whitelist'])

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#https://github.com/codebox/homoglyph/blob/master/raw_data/chars.txt
homoglypths = dict()
homoglypths['a'] = U'\u00c5\u0226\u00c4\u04d2\u0061\u0251\u03b1\u0430\u237a\uff41\U0001d41a\U0001d44e\U0001d482\U0001d4b6\U0001d4ea\U0001d51e\U0001d552\U0001d586\U0001d5ba\U0001d5ee\U0001d622\U0001d656\U0001d68a\U0001d6c2\U0001d6fc\U0001d736\U0001d770\U0001d7aa\u0041\u0391\u0410\u13aa\u15c5\u1d00\ua4ee\uab7a\uff21\U000102a0\U00016f40\U0001d400\U0001d434\U0001d468\U0001d49c\U0001d4d0\U0001d504\U0001d538\U0001d56c\U0001d5a0\U0001d5d4\U0001d608\U0001d63c\U0001d670\U0001d6a8\U0001d6e2\U0001d71c\U0001d756\U0001d790'
homoglypths['b'] = U'\u00df\u03b2\u03d0\u13f0\ua7b5\U0001d6c3\U0001d6fd\U0001d737\U0001d771\U0001d7ab\u0062\u0184\u042c\u13cf\u1472\u15af\uff42\U0001d41b\U0001d44f\U0001d483\U0001d4b7\U0001d4eb\U0001d51f\U0001d553\U0001d587\U0001d5bb\U0001d5ef\U0001d623\U0001d657\U0001d68b\u0042\u0299\u0392\u0412\u0432\u13f4\u13fc\u15f7\u16d2\u212c\ua4d0\ua7b4\uff22\U00010282\U000102a1\U00010301\U0001d401\U0001d435\U0001d469\U0001d4d1\U0001d505\U0001d539\U0001d56d\U0001d5a1\U0001d5d5\U0001d609\U0001d63d\U0001d671\U0001d6a9\U0001d6e3\U0001d71d\U0001d757\U0001d791'
homoglypths['c'] = U'\u00a9\u24b8\u0063\u03f2\u0441\u1d04\u217d\u2ca5\uabaf\uff43\U0001043d\U0001d41c\U0001d450\U0001d484\U0001d4b8\U0001d4ec\U0001d520\U0001d554\U0001d588\U0001d5bc\U0001d5f0\U0001d624\U0001d658\U0001d68c\u0043\u03f9\u0421\u13df\u1455\u2102\u212d\u216d\u2282\u2ca4\u2e26\ua4da\uff23\U000102a2\U00010302\U00010415\U0001051c\U000118e9\U000118f2\U0001d402\U0001d436\U0001d46a\U0001d49e\U0001d4d2\U0001d56e\U0001d5a2\U0001d5d6\U0001d60a\U0001d63e\U0001d672\U0001f74c'
homoglypths['d'] = U'\u0064\u0501\u13e7\u146f\u2146\u217e\ua4d2\uff44\U0001d41d\U0001d451\U0001d485\U0001d4b9\U0001d4ed\U0001d521\U0001d555\U0001d589\U0001d5bd\U0001d5f1\U0001d625\U0001d659\U0001d68d\u0044\u13a0\u15de\u15ea\u1d05\u2145\u216e\ua4d3\uab70\uff24\U0001d403\U0001d437\U0001d46b\U0001d49f\U0001d4d3\U0001d507\U0001d53b\U0001d56f\U0001d5a3\U0001d5d7\U0001d60b\U0001d63f\U0001d673'
homoglypths['e'] = U'\u00a3\u20a4\u0065\u0435\u04bd\u212e\u212f\u2147\uab32\uff45\U0001d41e\U0001d452\U0001d486\U0001d4ee\U0001d522\U0001d556\U0001d58a\U0001d5be\U0001d5f2\U0001d626\U0001d65a\U0001d68e\u0045\u0395\u0415\u13ac\u1d07\u2130\u22ff\u2d39\ua4f0\uab7c\uff25\U00010286\U000118a6\U000118ae\U0001d404\U0001d438\U0001d46c\U0001d4d4\U0001d508\U0001d53c\U0001d570\U0001d5a4\U0001d5d8\U0001d60c\U0001d640\U0001d674\U0001d6ac\U0001d6e6\U0001d720\U0001d75a\U0001d794'
homoglypths['f'] = U'\u0066\u017f\u03dd\u0584\u1e9d\ua799\uab35\uff46\U0001d41f\U0001d453\U0001d487\U0001d4bb\U0001d4ef\U0001d523\U0001d557\U0001d58b\U0001d5bf\U0001d5f3\U0001d627\U0001d65b\U0001d68f\U0001d7cb\u0046\u03dc\u15b4\u2131\ua4dd\ua798\uff26\U00010287\U000102a5\U00010525\U000118a2\U000118c2\U0001d213\U0001d405\U0001d439\U0001d46d\U0001d4d5\U0001d509\U0001d53d\U0001d571\U0001d5a5\U0001d5d9\U0001d60d\U0001d641\U0001d675\U0001d7ca'
homoglypths['g'] = U'\u0067\u018d\u0261\u0581\u1d83\u210a\uff47\U0001d420\U0001d454\U0001d488\U0001d4f0\U0001d524\U0001d558\U0001d58c\U0001d5c0\U0001d5f4\U0001d628\U0001d65c\U0001d690\u0047\u0262\u050c\u050d\u13c0\u13f3\u13fb\ua4d6\uab90\uff27\U0001d406\U0001d43a\U0001d46e\U0001d4a2\U0001d4d6\U0001d50a\U0001d53e\U0001d572\U0001d5a6\U0001d5da\U0001d60e\U0001d642\U0001d676'
homoglypths['h'] = U'\u0068\u04bb\u0570\u13c2\u210e\uff48\U0001d421\U0001d489\U0001d4bd\U0001d4f1\U0001d525\U0001d559\U0001d58d\U0001d5c1\U0001d5f5\U0001d629\U0001d65d\U0001d691\u0048\u029c\u0397\u041d\u043d\u13bb\u157c\u210b\u210c\u210d\u2c8e\ua4e7\uab8b\uff28\U000102cf\U0001d407\U0001d43b\U0001d46f\U0001d4d7\U0001d573\U0001d5a7\U0001d5db\U0001d60f\U0001d643\U0001d677\U0001d6ae\U0001d6e8\U0001d722\U0001d75c\U0001d796'
homoglypths['i'] = U'\u0069\u0131\u0269\u026a\u02db\u037a\u03b9\u0456\u04cf\u13a5\u1fbe\u2139\u2148\u2170\u2373\ua647\uab75\uff49\U000118c3\U0001d422\U0001d456\U0001d48a\U0001d4be\U0001d4f2\U0001d526\U0001d55a\U0001d58e\U0001d5c2\U0001d5f6\U0001d62a\U0001d65e\U0001d692\U0001d6a4\U0001d6ca\U0001d704\U0001d73e\U0001d778\U0001d7b2\u0031\u0049\u006c\u007c\u0196\u01c0\u0399\u0406\u04c0\u05c0\u05d5\u05df\u0627\u0661\u06f1\u07ca\u16c1\u2110\u2111\u2113\u2160\u217c\u2223\u23fd\u2c92\u2d4f\ua4f2\ufe8d\ufe8e\uff11\uff29\uff4c\uffe8\U0001028a\U00010309\U00010320\U00016f28\U0001d408\U0001d425\U0001d43c\U0001d459\U0001d470\U0001d48d\U0001d4c1\U0001d4d8\U0001d4f5\U0001d529\U0001d540\U0001d55d\U0001d574\U0001d591\U0001d5a8\U0001d5c5\U0001d5dc\U0001d5f9\U0001d610\U0001d62d\U0001d644\U0001d661\U0001d678\U0001d695\U0001d6b0\U0001d6ea\U0001d724\U0001d75e\U0001d798\U0001d7cf\U0001d7d9\U0001d7e3\U0001d7ed\U0001d7f7\U0001e8c7\U0001ee00\U0001ee80\U0001fbf1'
homoglypths['j'] = U'\u006a\u03f3\u0458\u2149\uff4a\U0001d423\U0001d457\U0001d48b\U0001d4bf\U0001d4f3\U0001d527\U0001d55b\U0001d58f\U0001d5c3\U0001d5f7\U0001d62b\U0001d65f\U0001d693\u004a\u037f\u0408\u13ab\u148d\u1d0a\ua4d9\ua7b2\uab7b\uff2a\U0001d409\U0001d43d\U0001d471\U0001d4a5\U0001d4d9\U0001d50d\U0001d541\U0001d575\U0001d5a9\U0001d5dd\U0001d611\U0001d645\U0001d679'
homoglypths['k'] = U'\u0138\u03ba\u03f0\u043a\u1d0b\u2c95\uabb6\U0001d6cb\U0001d6de\U0001d705\U0001d718\U0001d73f\U0001d752\U0001d779\U0001d78c\U0001d7b3\U0001d7c6\u006b\uff4b\U0001d424\U0001d458\U0001d48c\U0001d4c0\U0001d4f4\U0001d528\U0001d55c\U0001d590\U0001d5c4\U0001d5f8\U0001d62c\U0001d660\U0001d694\u004b\u039a\u041a\u13e6\u16d5\u212a\u2c94\ua4d7\uff2b\U00010518\U0001d40a\U0001d43e\U0001d472\U0001d4a6\U0001d4da\U0001d50e\U0001d542\U0001d576\U0001d5aa\U0001d5de\U0001d612\U0001d646\U0001d67a\U0001d6b1\U0001d6eb\U0001d725\U0001d75f\U0001d799'
homoglypths['l'] = U'\u004c\u029f\u13de\u14aa\u2112\u216c\u2cd0\u2cd1\ua4e1\uabae\uff2c\U0001041b\U00010443\U00010526\U000118a3\U000118b2\U00016f16\U0001d22a\U0001d40b\U0001d43f\U0001d473\U0001d4db\U0001d50f\U0001d543\U0001d577\U0001d5ab\U0001d5df\U0001d613\U0001d647\U0001d67b'
homoglypths['m'] = U'\u006d\uff4d\u004d\u039c\u03fa\u041c\u13b7\u15f0\u16d6\u2133\u216f\u2c98\ua4df\uff2d\U000102b0\U00010311\U0001d40c\U0001d440\U0001d474\U0001d4dc\U0001d510\U0001d544\U0001d578\U0001d5ac\U0001d5e0\U0001d614\U0001d648\U0001d67c\U0001d6b3\U0001d6ed\U0001d727\U0001d761\U0001d79b'
homoglypths['n'] = U'\u006e\u0578\u057c\uff4e\U0001d427\U0001d45b\U0001d48f\U0001d4c3\U0001d4f7\U0001d52b\U0001d55f\U0001d593\U0001d5c7\U0001d5fb\U0001d62f\U0001d663\U0001d697\u004e\u0274\u039d\u2115\u2c9a\ua4e0\uff2e\U00010513\U0001d40d\U0001d441\U0001d475\U0001d4a9\U0001d4dd\U0001d511\U0001d579\U0001d5ad\U0001d5e1\U0001d615\U0001d649\U0001d67d\U0001d6b4\U0001d6ee\U0001d728\U0001d762\U0001d79c'
homoglypths['o'] = U'\u00d6\u0150\u04e6\u0030\u004f\u006f\u039f\u03bf\u03c3\u041e\u043e\u0555\u0585\u05e1\u0647\u0665\u06be\u06c1\u06d5\u06f5\u07c0\u0966\u09e6\u0a66\u0ae6\u0b20\u0b66\u0be6\u0c02\u0c66\u0c82\u0ce6\u0d02\u0d20\u0d66\u0d82\u0e50\u0ed0\u101d\u1040\u10ff\u12d0\u1d0f\u1d11\u2134\u2c9e\u2c9f\u2d54\u3007\ua4f3\uab3d\ufba6\ufba7\ufba8\ufba9\ufbaa\ufbab\ufbac\ufbad\ufee9\ufeea\ufeeb\ufeec\uff10\uff2f\uff4f\U00010292\U000102ab\U00010404\U0001042c\U000104c2\U000104ea\U00010516\U000114d0\U000118b5\U000118c8\U000118d7\U000118e0\U0001d40e\U0001d428\U0001d442\U0001d45c\U0001d476\U0001d490\U0001d4aa\U0001d4de\U0001d4f8\U0001d512\U0001d52c\U0001d546\U0001d560\U0001d57a\U0001d594\U0001d5ae\U0001d5c8\U0001d5e2\U0001d5fc\U0001d616\U0001d630\U0001d64a\U0001d664\U0001d67e\U0001d698\U0001d6b6\U0001d6d0\U0001d6d4\U0001d6f0\U0001d70a\U0001d70e\U0001d72a\U0001d744\U0001d748\U0001d764\U0001d77e\U0001d782\U0001d79e\U0001d7b8\U0001d7bc\U0001d7ce\U0001d7d8\U0001d7e2\U0001d7ec\U0001d7f6\U0001ee24\U0001ee64\U0001ee84\U0001fbf0'
homoglypths['p'] = U'\u00de\u03f7\U000104c4\u0070\u03c1\u03f1\u0440\u2374\u2ca3\uff50\U0001d429\U0001d45d\U0001d491\U0001d4c5\U0001d4f9\U0001d52d\U0001d561\U0001d595\U0001d5c9\U0001d5fd\U0001d631\U0001d665\U0001d699\U0001d6d2\U0001d6e0\U0001d70c\U0001d71a\U0001d746\U0001d754\U0001d780\U0001d78e\U0001d7ba\U0001d7c8\u0050\u03a1\u0420\u13e2\u146d\u1d18\u1d29\u2119\u2ca2\ua4d1\uabb2\uff30\U00010295\U0001d40f\U0001d443\U0001d477\U0001d4ab\U0001d4df\U0001d513\U0001d57b\U0001d5af\U0001d5e3\U0001d617\U0001d64b\U0001d67f\U0001d6b8\U0001d6f2\U0001d72c\U0001d766\U0001d7a0'
homoglypths['q'] = U'\u0071\u051b\u0563\u0566\uff51\U0001d42a\U0001d45e\U0001d492\U0001d4c6\U0001d4fa\U0001d52e\U0001d562\U0001d596\U0001d5ca\U0001d5fe\U0001d632\U0001d666\U0001d69a\u0051\u211a\u2d55\uff31\U0001d410\U0001d444\U0001d478\U0001d4ac\U0001d4e0\U0001d514\U0001d57c\U0001d5b0\U0001d5e4\U0001d618\U0001d64c\U0001d680'
homoglypths['r'] = U'\u00ae\u24c7\u0072\u0433\u1d26\u2c85\uab47\uab48\uab81\uff52\U0001d42b\U0001d45f\U0001d493\U0001d4c7\U0001d4fb\U0001d52f\U0001d563\U0001d597\U0001d5cb\U0001d5ff\U0001d633\U0001d667\U0001d69b\u0052\u01a6\u0280\u13a1\u13d2\u1587\u16b1\u211b\u211c\u211d\ua4e3\uab71\uaba2\uff32\U000104b4\U00016f35\U0001d216\U0001d411\U0001d445\U0001d479\U0001d4e1\U0001d57d\U0001d5b1\U0001d5e5\U0001d619\U0001d64d\U0001d681'
homoglypths['s'] = U'\u0073\u01bd\u0455\ua731\uabaa\uff53\U00010448\U000118c1\U0001d42c\U0001d460\U0001d494\U0001d4c8\U0001d4fc\U0001d530\U0001d564\U0001d598\U0001d5cc\U0001d600\U0001d634\U0001d668\U0001d69c\u0053\u0405\u054f\u13d5\u13da\ua4e2\uff33\U00010296\U00010420\U00016f3a\U0001d412\U0001d446\U0001d47a\U0001d4ae\U0001d4e2\U0001d516\U0001d54a\U0001d57e\U0001d5b2\U0001d5e6\U0001d61a\U0001d64e\U0001d682'
homoglypths['t'] = U'\u0074\uff54\U0001d42d\U0001d461\U0001d495\U0001d4c9\U0001d4fd\U0001d531\U0001d565\U0001d599\U0001d5cd\U0001d601\U0001d635\U0001d669\U0001d69d\u0054\u03a4\u03c4\u0422\u0442\u13a2\u1d1b\u22a4\u27d9\u2ca6\ua4d4\uab72\uff34\U00010297\U000102b1\U00010315\U000118bc\U00016f0a\U0001d413\U0001d447\U0001d47b\U0001d4af\U0001d4e3\U0001d517\U0001d54b\U0001d57f\U0001d5b3\U0001d5e7\U0001d61b\U0001d64f\U0001d683\U0001d6bb\U0001d6d5\U0001d6f5\U0001d70f\U0001d72f\U0001d749\U0001d769\U0001d783\U0001d7a3\U0001d7bd\U0001f768'
homoglypths['u'] = U'\u00b5\u03bc\U0001d6cd\U0001d707\U0001d741\U0001d77b\U0001d7b5\u0075\u028b\u03c5\u057d\u1d1c\ua79f\uab4e\uab52\uff55\U000104f6\U000118d8\U0001d42e\U0001d462\U0001d496\U0001d4ca\U0001d4fe\U0001d532\U0001d566\U0001d59a\U0001d5ce\U0001d602\U0001d636\U0001d66a\U0001d69e\U0001d6d6\U0001d710\U0001d74a\U0001d784\U0001d7be\u0055\u054d\u1200\u144c\u222a\u22c3\ua4f4\uff35\U000104ce\U000118b8\U00016f42\U0001d414\U0001d448\U0001d47c\U0001d4b0\U0001d4e4\U0001d518\U0001d54c\U0001d580\U0001d5b4\U0001d5e8\U0001d61c\U0001d650\U0001d684'
homoglypths['v'] = U'\u0076\u03bd\u0475\u05d8\u1d20\u2174\u2228\u22c1\uaba9\uff56\U00011706\U000118c0\U0001d42f\U0001d463\U0001d497\U0001d4cb\U0001d4ff\U0001d533\U0001d567\U0001d59b\U0001d5cf\U0001d603\U0001d637\U0001d66b\U0001d69f\U0001d6ce\U0001d708\U0001d742\U0001d77c\U0001d7b6\u0056\u0474\u0667\u06f7\u13d9\u142f\u2164\u2d38\ua4e6\ua6df\uff36\U0001051d\U000118a0\U00016f08\U0001d20d\U0001d415\U0001d449\U0001d47d\U0001d4b1\U0001d4e5\U0001d519\U0001d54d\U0001d581\U0001d5b5\U0001d5e9\U0001d61d\U0001d651\U0001d685'
homoglypths['w'] = U'\u0077\u026f\u0461\u051d\u0561\u1d21\uab83\uff57\U0001170a\U0001170e\U0001170f\U0001d430\U0001d464\U0001d498\U0001d4cc\U0001d500\U0001d534\U0001d568\U0001d59c\U0001d5d0\U0001d604\U0001d638\U0001d66c\U0001d6a0\u0057\u051c\u13b3\u13d4\ua4ea\uff37\U000118e6\U000118ef\U0001d416\U0001d44a\U0001d47e\U0001d4b2\U0001d4e6\U0001d51a\U0001d54e\U0001d582\U0001d5b6\U0001d5ea\U0001d61e\U0001d652\U0001d686'
homoglypths['x'] = U'\u0078\u00d7\u0445\u1541\u157d\u166e\u2179\u292b\u292c\u2a2f\uff58\U0001d431\U0001d465\U0001d499\U0001d4cd\U0001d501\U0001d535\U0001d569\U0001d59d\U0001d5d1\U0001d605\U0001d639\U0001d66d\U0001d6a1\u0058\u03a7\u0425\u166d\u16b7\u2169\u2573\u2cac\u2d5d\ua4eb\ua7b3\uff38\U00010290\U000102b4\U00010317\U00010322\U00010527\U000118ec\U0001d417\U0001d44b\U0001d47f\U0001d4b3\U0001d4e7\U0001d51b\U0001d54f\U0001d583\U0001d5b7\U0001d5eb\U0001d61f\U0001d653\U0001d687\U0001d6be\U0001d6f8\U0001d732\U0001d76c\U0001d7a6'
homoglypths['y'] = U'\u0079\u0263\u028f\u03b3\u0443\u04af\u10e7\u1d8c\u1eff\u213d\uab5a\uff59\U000118dc\U0001d432\U0001d466\U0001d49a\U0001d4ce\U0001d502\U0001d536\U0001d56a\U0001d59e\U0001d5d2\U0001d606\U0001d63a\U0001d66e\U0001d6a2\U0001d6c4\U0001d6fe\U0001d738\U0001d772\U0001d7ac\u0059\u03a5\u03d2\u0423\u04ae\u13a9\u13bd\u2ca8\ua4ec\uff39\U000102b2\U000118a4\U00016f43\U0001d418\U0001d44c\U0001d480\U0001d4b4\U0001d4e8\U0001d51c\U0001d550\U0001d584\U0001d5b8\U0001d5ec\U0001d620\U0001d654\U0001d688\U0001d6bc\U0001d6f6\U0001d730\U0001d76a\U0001d7a4'
homoglypths['z'] = U'\u007a\u1d22\uab93\uff5a\U000118c4\U0001d433\U0001d467\U0001d49b\U0001d4cf\U0001d503\U0001d537\U0001d56b\U0001d59f\U0001d5d3\U0001d607\U0001d63b\U0001d66f\U0001d6a3\u005a\u0396\u13c3\u2124\u2128\ua4dc\uff3a\U000102f5\U000118a9\U000118e5\U0001d419\U0001d44d\U0001d481\U0001d4b5\U0001d4e9\U0001d585\U0001d5b9\U0001d5ed\U0001d621\U0001d655\U0001d689\U0001d6ad\U0001d6e7\U0001d721\U0001d75b\U0001d795'

banned_words = config.get('banned_words', [])
allowed_roles = config.get('allowed_roles', [])
whitelist = config.get('whitelist', {})
banned_users = config.get('banned_users', {})

notif_channel = None

last_massban = None
last_massban_ts = -1
last_massban_mod = None

def standardize_string(s: str) -> str:
    standardized = ''
    for c in s:
        default = True
        for char, values in homoglypths.items():
            if c in values:
                default = False
                standardized += char
        if default:
            standardized += c
    # simplify similar characters further
    return standardized.replace('e', 'c')\
                       .replace('y','v')\
                       .replace('u','v')\
                       .replace('vv', 'w')\
                       .replace('i', 'l')\
                       .replace('1', 'l')\
                       .replace('0', 'o')
    
def add_banned_word(s: str):
    banned_words.append(s)
    banned_words_converted.append(standardize_string(s))
    config.save_config()
    
def remove_banned_word(s: str):
    banned_words.remove(s)
    banned_words_converted.remove(standardize_string(s))
    config.save_config()

# Should be okay as list since relatively low number of words
banned_words_converted = [standardize_string(s) for s in banned_words]


user_ids = []
user_names_standardized = []
modmail_blacklist = dict()
def maybe_blacklist_modmail_name(user_id: int, user_name: str):
    global user_ids, user_names_standardized, modmail_blacklist
    if user_id in user_ids:
        return
    standardized_to_check = standardize_string(user_name)
    if standardized_to_check in user_names_standardized:
        # If we find the same standardized name within 10 modmail requests (spam), mark it blocked for one hour
        modmail_blacklist[standardized_to_check] = time.time()
        print(f'Blocked f{standardized_to_check} for 1h.')
    elif len(user_ids) > 10:
        user_ids = user_ids[1:]
        user_names_standardized = user_names_standardized[1:]
        user_ids.append(user_id)
        user_names_standardized.append(standardized_to_check)

@client.event
async def on_ready():
    global notif_channel
    game = discord.Game("Checking For Scammers")
    await client.change_presence(status=discord.Status.idle, activity=game)
    guild_id = config.get('guild', None)
    if guild_id:
        channel_id = config.get('channel', None)
        if channel_id:
            notif_guild = await client.fetch_guild(guild_id)
            channels = await notif_guild.fetch_channels()
            for channel in channels:
                if channel.id == channel_id:
                    notif_channel = channel
                    break
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_update(before, after):
    if not notif_channel:
        return
    if after.name in whitelist:
        return
    standardized = standardize_string(after.name) 
    for i, word in enumerate(banned_words_converted):
        if word in standardized:
            print(after.name)
            print('Changed bad')
            invite = await notif_channel.create_invite()
            await after.create_dm()
            await after.dm_channel.send(
                    f'Hello {after.name},\nUnfortunately you have been KICKED for having the word "{banned_words[i]}" in your name (or similar).\nPlease change your name before attempting to rejoin the server or you will be banned.\n{invite.url}'
                )
            await notif_channel.guild.kick(after)
            return

@client.event
async def on_member_join(member):

    if member.guild.id == 884176665511624786:  # Hardcoded shared server
        return

    if member.name in whitelist:
        return

    converted_name = standardize_string(member.name)
    for i, word in enumerate(banned_words_converted):
        if word in converted_name:
            await member.create_dm()
            await member.dm_channel.send(
                    f'Hello {member.name},\nUnfortunately you have been BANNED for having the word "{banned_words[i]}" in your name (or similar).\nIf you believe this to be an error, please join https://discord.gg/yaAGGVFtXp then please respond in this DM.'
                )
            await member.guild.ban(member, reason='bad name')
            return 

# TODO: Make this better
channel_cache = dict()
@client.event
async def on_message(message):
    global notif_channel, channel_cache, banned_users
    if message.author == client.user or message.author.id in banned_users:
        return
    
    if notif_channel and message.channel == notif_channel and message.reference and message.author.guild_permissions.ban_members:
        msg = message.reference.cached_message
        if not msg:
            msg = await notif_channel.fetch_message(message.reference.message_id)
        if msg.author != client.user:
            return
        if message.content == '!raven doubleban':
            banned_users.add(message.author.id)
            await notif_channel.send("Banned. No more messages will be recieved from them.")
            return
        elif message.content == '!raven unban':
            person = client.get_user(int(msg.content))
            if not person:
                person = await client.fetch_user(int(msg.content))

            whitelist.add(person.name)
            await notif_channel.guild.unban(person)
            await notif_channel.send("User unbanned.")
            # TODO: Find a better way to do this
            for chan in client.private_channels:
                if chan.recipient.id == int(msg.content):
                    invite = await notif_channel.create_invite()
                    await chan.send(f'You have been unbanned! Please rejoin here: {invite.url}')
                    return

            return
        else:
            # TODO: Find a better way to do this
            for chan in client.private_channels:
                if chan.recipient.id == int(msg.content):
                    await chan.send(message.content)
                    return

    if isinstance(message.channel, discord.DMChannel):
        if not notif_channel:
            print("Tried to notify, but no notify channel!!!\n\n{}\n{}".format(message.channel.recipient.id, message.content))
            return
        # See if there's a way not to make these API calls
        #member = await notif_channel.guild.fetch_member(message.channel.recipient.id)
        #try:
        #    ban = await notif_channel.guild.fetch_ban(member)
        #except:
        #    ban = None
        #if not ban:
            # User is not banned, do not communicate
        #    return

        global modmail_blacklist
        maybe_blacklist_modmail_name(message.channel.recipient.id, message.channel.recipient.name)
        s_name = standardize_string(message.channel.recipient.name)
        if s_name in modmail_blacklist:
            last_ts = modmail_blacklist[s_name]
            delta = time.time() - last_ts
            if delta > 60 * 60:
                del modmail_blacklist[s_name]
            else:
                await message.channel.send('You are currently unable to send modmail messages due to multiple accounts having your same name making requests. Please try again in an hour.')
                return
        
        embed = discord.Embed()
        embed.set_author(name='#'.join([str(message.channel.recipient.name),str(message.channel.recipient.discriminator)]))
        embed.add_field(name='Message', value=message.content, inline=True)
        embed.set_footer(text='Reply to this message to reply to this user. Reply with !raven doubleban to prevent this user from messaging. Reply with !raven unban to unban this user, whitelist their name, and give them an invite back to the server.')

        await notif_channel.send(message.channel.recipient.id, embed=embed)
        return

    content = str(message.content).split(' ')

    tri = len(content) >= 3

    if content[0] == '!raven':

        # Only users who have permission to ban users in the discord may use this bot.
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(f"<@{message.author.id}> you do not have permission to send RavenBot commands!")
            return

        if content[1] == 'addword' and tri:
            add_banned_word(content[2])
            await message.channel.send(f"{content[2]} added to the banned words list.")
        elif content[1] == 'removeword' and tri:
            if content[2] in banned_words:
                remove_banned_word(content[2])
                await message.channel.send(f"{content[2]} removed from the banned words list.")
            else:
                await message.channel.send(f"{content[2]} is not in the banned words list!")
        elif content[1] == 'words':
            await message.channel.send(f"{banned_words}")
        elif content[1] == 'channel':
            config['channel'] = message.channel.id
            config['guild'] = message.channel.guild.id
            notif_channel = message.channel
            await message.channel.send("Notifications will now be sent to this channel.")
        elif content[1] == 'unchannel':
            config['channel'] = None
            notif_channel = None
            await message.channel.send("Notifications will no longer be sent.")
        elif content[1] == 'massban' and tri:
            global last_massban, last_massban_ts, last_massban_mod

            send_info = False

            if last_massban != content[2]:
                send_info = True
                last_massban = content[2]
                last_massban_ts = time.time()
                last_massban_mod = message.author
            elif time.time() - last_massban_ts > 60:
                send_info = True
                last_massban_ts = time.time()
                last_massban_mod = message.author
            elif last_massban_mod == message.author:
                send_info = True

            if send_info:
                await message.channel.send("Two moderators must type the same massban command within 1 minute in order for it to execute.")
                return

            last_massban = None
            last_massban_ts = -1
            last_massban_author = None

            standard_test = standardize_string(" ".join(content[2:]).replace("\"","").lower())

            for bad in [x for x in message.channel.guild.members if standardize_string(x.name) == standard_test]:
                await bad.create_dm()
                await bad.dm_channel.send(
                    f'Hello {bad.name},\nUnfortunately you have been banned in a mass ban based on name.\nIf you believe this to be an error, please join https://discord.gg/yaAGGVFtXp then please respond in this DM.'
                )
                await message.channel.guild.ban(bad, reason='mass ban')
        elif content[1] == 'help':
            await message.channel.send("addword, removeword, words, channel, unchannel, massban")
        else:
            await message.channel.send("Unknown command!")

client.run(TOKEN)
