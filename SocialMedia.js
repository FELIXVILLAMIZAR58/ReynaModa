import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Instagram, Send, Clock, CheckCircle, AlertCircle,
  Sparkles, Image, Zap, Link, Upload, RefreshCw
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ── helpers ──────────────────────────────────────────────────────────────────
const authHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('reyna_admin_token')}`
});

const SocialMedia = () => {
  const [activeTab, setActiveTab] = useState('accounts');

  const tabs = [
    { id: 'accounts',  label: 'Cuentas'    },
    { id: 'create',    label: 'Crear con IA' },
    { id: 'schedule',  label: 'Programar'  },
    { id: 'history',   label: 'Historial'  },
  ];

  return (
    <div data-testid="social-media-module">
      <h1 className="text-4xl font-black italic uppercase mb-8">
        Marketing <span className="text-[#D4AF37]">Social</span>
      </h1>

      {/* Tab bar */}
      <div className="flex gap-2 bg-white/5 p-2 rounded-full border border-white/10 mb-8 overflow-x-auto">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`px-6 py-3 rounded-full text-[9px] font-black uppercase tracking-widest transition-all whitespace-nowrap ${
              activeTab === t.id
                ? 'bg-[#D4AF37] text-black'
                : 'text-gray-500 hover:text-white'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {activeTab === 'accounts'  && <AccountsTab />}
      {activeTab === 'create'    && <CreateContentTab />}
      {activeTab === 'schedule'  && <ScheduleTab />}
      {activeTab === 'history'   && <HistoryTab />}
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// TAB 1 – CUENTAS CONECTADAS
// ════════════════════════════════════════════════════════════════════════════
const AccountsTab = () => {
  const [status, setStatus]   = useState({});
  const [igForm, setIgForm]   = useState({ accessToken: '', businessAccountId: '' });
  const [waForm, setWaForm]   = useState({ phoneNumberId: '', accessToken: '' });
  const [saving, setSaving]   = useState('');
  const [msg, setMsg]         = useState('');

  useEffect(() => { fetchStatus(); }, []);

  const fetchStatus = async () => {
    try {
      const r = await axios.get(`${API}/social/status`, { headers: authHeaders() });
      setStatus(r.data);
    } catch {}
  };

  const saveInstagram = async () => {
    setSaving('ig');
    try {
      await axios.post(`${API}/social/connect/instagram`, igForm, { headers: authHeaders() });
      setMsg('Instagram conectado ✓');
      fetchStatus();
    } catch (e) {
      setMsg(e.response?.data?.detail || 'Error al conectar Instagram');
    } finally { setSaving(''); }
  };

  const saveWhatsApp = async () => {
    setSaving('wa');
    try {
      await axios.post(`${API}/social/connect/whatsapp`, waForm, { headers: authHeaders() });
      setMsg('WhatsApp API conectado ✓');
      fetchStatus();
    } catch (e) {
      setMsg(e.response?.data?.detail || 'Error al conectar WhatsApp');
    } finally { setSaving(''); }
  };

  const Connected = ({ platform }) => status[platform]?.connected
    ? <span className="px-3 py-1 rounded-full text-[8px] font-black uppercase bg-green-500/20 text-green-400 border border-green-500/20">Conectado</span>
    : <span className="px-3 py-1 rounded-full text-[8px] font-black uppercase bg-yellow-500/20 text-yellow-400 border border-yellow-500/20">Sin conectar</span>;

  return (
    <div className="space-y-6">
      {msg && (
        <div className="bg-green-500/10 border border-green-500/20 rounded-2xl p-4 text-sm text-green-400">
          {msg}
        </div>
      )}

      {/* Aviso general */}
      <div className="bg-[#D4AF37]/10 border border-[#D4AF37]/20 rounded-3xl p-6">
        <p className="text-sm text-[#D4AF37] font-bold mb-1">💰 Costo total de este módulo: $0</p>
        <p className="text-xs text-gray-400">
          Instagram Graph API, WhatsApp Cloud API y APScheduler son gratuitos para el volumen de REYNA MODA.
          TikTok funciona con envío al celular del admin — sin costo ni aprobación.
        </p>
      </div>

      {/* Instagram */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-yellow-500 via-[#FF007F] to-fuchsia-800 flex items-center justify-center">
              <Instagram size={20} className="text-white" />
            </div>
            <div>
              <p className="font-bold text-sm">Instagram Business</p>
              <p className="text-[9px] text-gray-500 uppercase">Meta Graph API — publicación directa gratis</p>
            </div>
          </div>
          <Connected platform="instagram" />
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Access Token</label>
            <input
              type="password"
              value={igForm.accessToken}
              onChange={e => setIgForm({ ...igForm, accessToken: e.target.value })}
              placeholder="EAABsbCS0..."
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-xs focus:border-[#D4AF37] outline-none"
            />
          </div>
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Instagram Business Account ID</label>
            <input
              type="text"
              value={igForm.businessAccountId}
              onChange={e => setIgForm({ ...igForm, businessAccountId: e.target.value })}
              placeholder="17841400455970153"
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-xs focus:border-[#D4AF37] outline-none"
            />
          </div>
        </div>
        <div className="mt-4 p-3 bg-black/40 rounded-xl text-[10px] text-gray-500 leading-relaxed">
          <strong className="text-gray-300">Cómo obtenerlo:</strong> Ve a{' '}
          <a href="https://developers.facebook.com" target="_blank" rel="noreferrer" className="text-[#D4AF37] underline">developers.facebook.com</a>
          {' '}→ Nueva App → Business → Agrega "Instagram" → Genera Access Token de larga duración.
          Requiere cuenta Business o Creator + Página de Facebook vinculada.
        </div>
        <button
          onClick={saveInstagram}
          disabled={saving === 'ig' || !igForm.accessToken}
          className="mt-4 px-6 py-3 bg-[#D4AF37] text-black font-black text-xs uppercase rounded-full hover:scale-105 transition-transform disabled:opacity-50"
        >
          {saving === 'ig' ? 'Guardando...' : 'Guardar configuración'}
        </button>
      </div>

      {/* WhatsApp */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-green-500/20 flex items-center justify-center">
              <Send size={20} className="text-green-400" />
            </div>
            <div>
              <p className="font-bold text-sm">WhatsApp Cloud API</p>
              <p className="text-[9px] text-gray-500 uppercase">Meta — gratis hasta 1000 conv/mes</p>
            </div>
          </div>
          <Connected platform="whatsapp" />
        </div>
        <div className="bg-[#D4AF37]/10 rounded-xl p-3 mb-4 text-[10px] text-[#D4AF37]">
          Sin API: el sistema sigue funcionando con links wa.me (flujo actual). La API agrega confirmaciones automáticas de pedidos.
        </div>
        <div className="space-y-3">
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Phone Number ID</label>
            <input
              type="text"
              value={waForm.phoneNumberId}
              onChange={e => setWaForm({ ...waForm, phoneNumberId: e.target.value })}
              placeholder="114746175423858"
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-xs focus:border-[#D4AF37] outline-none"
            />
          </div>
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Access Token</label>
            <input
              type="password"
              value={waForm.accessToken}
              onChange={e => setWaForm({ ...waForm, accessToken: e.target.value })}
              placeholder="EAABsbCS0..."
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-xs focus:border-[#D4AF37] outline-none"
            />
          </div>
        </div>
        <div className="mt-4 p-3 bg-black/40 rounded-xl text-[10px] text-gray-500 leading-relaxed">
          <strong className="text-gray-300">Cómo obtenerlo:</strong> En la misma app de Meta Developers → Agrega producto "WhatsApp" → En "Configuración" encuentras el Phone Number ID y el Token temporal. Para un token permanente ve a Configuración de App → Básica → genera token con permisos whatsapp_business_messaging.
        </div>
        <button
          onClick={saveWhatsApp}
          disabled={saving === 'wa' || !waForm.phoneNumberId}
          className="mt-4 px-6 py-3 bg-green-500 text-black font-black text-xs uppercase rounded-full hover:scale-105 transition-transform disabled:opacity-50"
        >
          {saving === 'wa' ? 'Guardando...' : 'Guardar configuración'}
        </button>
      </div>

      {/* TikTok */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/10 flex items-center justify-center font-black text-xs">TT</div>
            <div>
              <p className="font-bold text-sm">TikTok</p>
              <p className="text-[9px] text-gray-500 uppercase">Semi-automático — 1 toque desde tu celular</p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-[8px] font-black uppercase bg-blue-500/20 text-blue-400 border border-blue-500/20">Listo sin configurar</span>
        </div>
        <div className="p-3 bg-blue-500/10 rounded-xl text-[10px] text-blue-300 leading-relaxed">
          <strong>¿Cómo funciona?</strong> La IA genera el caption y hashtags → el sistema lo envía a tu WhatsApp (3167470857) → tú abres TikTok, pegas el texto y publicas. No requiere API ni aprobación. Costo: $0.
        </div>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// TAB 2 – CREAR CONTENIDO CON IA
// ════════════════════════════════════════════════════════════════════════════
const CreateContentTab = () => {
  const [products, setProducts]   = useState([]);
  const [form, setForm]           = useState({
    productId: '', contentType: 'post', tone: 'elegant'
  });
  const [generated, setGenerated] = useState(null);
  const [loading, setLoading]     = useState(false);
  const [bgFile, setBgFile]       = useState(null);
  const [bgResult, setBgResult]   = useState(null);
  const [bgLoading, setBgLoading] = useState(false);
  const fileRef = useRef();

  useEffect(() => {
    axios.get(`${API}/products`).then(r => setProducts(r.data));
  }, []);

  const selectedProduct = products.find(p => p.id === form.productId) || products[0];

  const generate = async () => {
    if (!selectedProduct) return;
    setLoading(true);
    try {
      const r = await axios.post(`${API}/social/generate-content`, {
        productName: selectedProduct.name,
        category:    selectedProduct.category,
        price:       selectedProduct.price,
        salePrice:   selectedProduct.salePrice,
        tags:        selectedProduct.tags,
        contentType: form.contentType,
        tone:        form.tone,
      }, { headers: authHeaders() });
      setGenerated(r.data);
    } catch (e) {
      alert('Error al generar contenido: ' + (e.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  };

  const removeBackground = async () => {
    if (!bgFile) return;
    setBgLoading(true);
    try {
      const fd = new FormData();
      fd.append('file', bgFile);
      const r = await axios.post(`${API}/social/remove-background`, fd, {
        headers: { ...authHeaders(), 'Content-Type': 'multipart/form-data' },
        responseType: 'blob',
      });
      setBgResult(URL.createObjectURL(r.data));
    } catch (e) {
      alert('Error: ' + (e.response?.data?.detail || e.message));
    } finally { setBgLoading(false); }
  };

  const contentTypes = [
    { id: 'post',  label: 'Post feed',    sub: 'Instagram / Facebook' },
    { id: 'reel',  label: 'Reel / TikTok', sub: 'Video corto 15–30s'  },
    { id: 'story', label: 'Story',         sub: '24 horas'            },
    { id: 'promo', label: 'Oferta',        sub: 'Urgencia + precio'   },
  ];

  const tones = [
    { id: 'elegant',  label: 'Elegante'  },
    { id: 'fun',      label: 'Divertido' },
    { id: 'urgent',   label: 'Urgente'   },
    { id: 'romantic', label: 'Romántico' },
  ];

  return (
    <div className="space-y-6">
      {/* Selección producto */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <label className="text-[9px] font-black uppercase text-gray-500 mb-2 block">Producto</label>
        <select
          value={form.productId}
          onChange={e => setForm({ ...form, productId: e.target.value })}
          className="w-full bg-black border border-white/10 rounded-2xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
        >
          {products.map(p => (
            <option key={p.id} value={p.id}>{p.name} — ${p.price?.toLocaleString()}</option>
          ))}
        </select>

        {/* Tipo de contenido */}
        <label className="text-[9px] font-black uppercase text-gray-500 mb-2 mt-4 block">Tipo de contenido</label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {contentTypes.map(ct => (
            <button
              key={ct.id}
              onClick={() => setForm({ ...form, contentType: ct.id })}
              className={`p-3 rounded-2xl border text-left transition-all ${
                form.contentType === ct.id
                  ? 'border-[#D4AF37] bg-[#D4AF37]/10'
                  : 'border-white/10 hover:border-white/20'
              }`}
            >
              <p className="text-xs font-bold">{ct.label}</p>
              <p className="text-[9px] text-gray-500 mt-0.5">{ct.sub}</p>
            </button>
          ))}
        </div>

        {/* Tono */}
        <label className="text-[9px] font-black uppercase text-gray-500 mb-2 mt-4 block">Tono</label>
        <div className="flex gap-2 flex-wrap">
          {tones.map(t => (
            <button
              key={t.id}
              onClick={() => setForm({ ...form, tone: t.id })}
              className={`px-4 py-2 rounded-full text-xs font-bold border transition-all ${
                form.tone === t.id
                  ? 'bg-[#FF007F] border-[#FF007F] text-white'
                  : 'border-white/10 text-gray-400 hover:text-white'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <button
          onClick={generate}
          disabled={loading}
          className="mt-6 flex items-center gap-2 px-8 py-4 bg-[#D4AF37] text-black font-black uppercase text-xs rounded-full hover:scale-105 transition-transform disabled:opacity-50"
        >
          <Sparkles size={16} />
          {loading ? 'Generando...' : 'Generar con IA'}
        </button>
      </div>

      {/* Resultado */}
      {generated && (
        <div className="bg-white/5 rounded-[30px] border border-white/10 p-6 space-y-4">
          <h3 className="font-black uppercase text-sm text-[#D4AF37]">Contenido generado</h3>

          {generated.tiktokHook && (
            <div>
              <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">🎬 Gancho TikTok (primeros 3s)</label>
              <div className="bg-black/60 rounded-xl p-3 text-sm font-bold">{generated.tiktokHook}</div>
            </div>
          )}

          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Caption</label>
            <textarea
              defaultValue={generated.caption}
              rows={5}
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
            />
          </div>

          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Hashtags</label>
            <textarea
              defaultValue={generated.hashtags}
              rows={2}
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-xs focus:border-[#D4AF37] outline-none"
            />
          </div>

          <div className="flex gap-3 flex-wrap">
            <button
              onClick={() => navigator.clipboard.writeText(generated.fullPost)}
              className="flex items-center gap-2 px-5 py-3 bg-white/5 border border-white/10 rounded-full text-xs font-bold hover:bg-white/10 transition-all"
            >
              <Link size={14} /> Copiar todo
            </button>
            <button
              onClick={() => {
                const url = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(generated.fullPost)}`;
                window.open(url, '_blank');
              }}
              className="flex items-center gap-2 px-5 py-3 bg-green-500/20 border border-green-500/20 text-green-400 rounded-full text-xs font-bold hover:bg-green-500/30 transition-all"
            >
              <Send size={14} /> Enviar a WhatsApp
            </button>
          </div>
        </div>
      )}

      {/* Remover fondo */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <h3 className="font-black uppercase text-sm mb-1">Remover fondo con IA</h3>
        <p className="text-xs text-gray-500 mb-4">Sube la foto del producto y la IA elimina el fondo automáticamente. 100% gratuito, corre en tu servidor.</p>

        <div
          className="border-2 border-dashed border-white/20 rounded-2xl p-8 text-center cursor-pointer hover:border-[#D4AF37] transition-all"
          onClick={() => fileRef.current?.click()}
        >
          <Upload className="mx-auto mb-2 text-gray-600" size={32} />
          <p className="text-sm text-gray-500">{bgFile ? bgFile.name : 'Haz clic o arrastra la imagen aquí'}</p>
          <input ref={fileRef} type="file" accept="image/*" className="hidden"
            onChange={e => setBgFile(e.target.files[0])} />
        </div>

        {bgFile && (
          <button
            onClick={removeBackground}
            disabled={bgLoading}
            className="mt-4 flex items-center gap-2 px-6 py-3 bg-[#FF007F] text-white font-black text-xs uppercase rounded-full hover:scale-105 transition-transform disabled:opacity-50"
          >
            <Image size={16} />
            {bgLoading ? 'Procesando...' : 'Remover fondo'}
          </button>
        )}

        {bgResult && (
          <div className="mt-4">
            <p className="text-[9px] text-gray-500 uppercase mb-2">Resultado:</p>
            <img src={bgResult} alt="Sin fondo" className="max-w-xs rounded-2xl border border-white/10" style={{ background: 'repeating-conic-gradient(#333 0% 25%, #222 0% 50%) 0 0 / 20px 20px' }} />
            <a href={bgResult} download="producto-sin-fondo.png"
              className="mt-2 inline-flex items-center gap-2 px-5 py-3 bg-white/5 border border-white/10 rounded-full text-xs font-bold hover:bg-white/10 transition-all">
              Descargar PNG
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

const ADMIN_WHATSAPP = '573167470857';

// ════════════════════════════════════════════════════════════════════════════
// TAB 3 – PROGRAMAR PUBLICACIÓN
// ════════════════════════════════════════════════════════════════════════════
const ScheduleTab = () => {
  const [form, setForm] = useState({
    caption: '', hashtags: '', imageUrl: '',
    platforms: ['instagram'],
    scheduledAt: '', productName: ''
  });
  const [loading, setLoading]     = useState(false);
  const [scheduled, setScheduled] = useState([]);
  const [msg, setMsg]             = useState('');

  useEffect(() => { fetchScheduled(); }, []);

  const fetchScheduled = async () => {
    try {
      const r = await axios.get(`${API}/social/scheduled`, { headers: authHeaders() });
      setScheduled(r.data);
    } catch {}
  };

  const togglePlatform = (p) => {
    setForm(f => ({
      ...f,
      platforms: f.platforms.includes(p)
        ? f.platforms.filter(x => x !== p)
        : [...f.platforms, p]
    }));
  };

  const submit = async (now = false) => {
    setLoading(true);
    try {
      const payload = { ...form, scheduledAt: now ? null : form.scheduledAt || null };
      const r = await axios.post(`${API}/social/schedule`, payload, { headers: authHeaders() });
      setMsg(r.data.message);
      fetchScheduled();
    } catch (e) {
      setMsg(e.response?.data?.detail || 'Error al programar');
    } finally { setLoading(false); }
  };

  const platforms = [
    { id: 'instagram', label: 'Instagram', color: 'from-yellow-500 via-[#FF007F] to-fuchsia-800' },
    { id: 'tiktok',    label: 'TikTok',    color: 'from-gray-700 to-gray-900' },
    { id: 'whatsapp',  label: 'WhatsApp',  color: 'from-green-700 to-green-500' },
  ];

  const bestTimes = [
    { day: 'Lun–Vie', time: '12pm–1pm',  level: 'Alto',   color: 'text-green-400' },
    { day: 'Jue–Vie', time: '7pm–9pm',   level: 'Máximo', color: 'text-[#D4AF37]' },
    { day: 'Sábado',  time: '10am–12pm', level: 'Medio',  color: 'text-yellow-500' },
  ];

  return (
    <div className="space-y-6">
      {msg && (
        <div className="bg-green-500/10 border border-green-500/20 rounded-2xl p-4 text-sm text-green-400">{msg}</div>
      )}

      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6 space-y-4">
        <h3 className="font-black uppercase text-sm">Nueva publicación</h3>

        <div>
          <label className="text-[9px] font-black uppercase text-gray-500 mb-2 block">Publicar en</label>
          <div className="flex gap-3 flex-wrap">
            {platforms.map(p => (
              <button
                key={p.id}
                onClick={() => togglePlatform(p.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold border transition-all ${
                  form.platforms.includes(p.id)
                    ? 'border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37]'
                    : 'border-white/10 text-gray-500 hover:text-white'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Caption</label>
          <textarea
            value={form.caption}
            onChange={e => setForm({ ...form, caption: e.target.value })}
            rows={4}
            placeholder="Pega aquí el caption generado por la IA o escribe uno nuevo..."
            className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
          />
        </div>

        <div>
          <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Hashtags</label>
          <input
            value={form.hashtags}
            onChange={e => setForm({ ...form, hashtags: e.target.value })}
            placeholder="#ReynaModa #ModaColombiana..."
            className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
          />
        </div>

        <div>
          <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">URL de imagen</label>
          <input
            value={form.imageUrl}
            onChange={e => setForm({ ...form, imageUrl: e.target.value })}
            placeholder="https://... (imagen del producto)"
            className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Fecha</label>
            <input
              type="date"
              value={form.scheduledAt?.split('T')[0] || ''}
              onChange={e => setForm({ ...form, scheduledAt: `${e.target.value}T${form.scheduledAt?.split('T')[1] || '12:00'}:00` })}
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
            />
          </div>
          <div>
            <label className="text-[9px] font-black uppercase text-gray-500 mb-1 block">Hora</label>
            <input
              type="time"
              value={form.scheduledAt?.split('T')[1]?.slice(0,5) || '12:00'}
              onChange={e => setForm({ ...form, scheduledAt: `${form.scheduledAt?.split('T')[0] || new Date().toISOString().split('T')[0]}T${e.target.value}:00` })}
              className="w-full bg-black border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-[#D4AF37] outline-none"
            />
          </div>
        </div>

        <div className="flex gap-3 flex-wrap">
          <button
            onClick={() => submit(false)}
            disabled={loading || !form.caption}
            className="flex items-center gap-2 px-6 py-3 bg-[#D4AF37] text-black font-black text-xs uppercase rounded-full hover:scale-105 transition-transform disabled:opacity-50"
          >
            <Clock size={14} />
            {loading ? 'Procesando...' : 'Programar publicación'}
          </button>
          <button
            onClick={() => submit(true)}
            disabled={loading || !form.caption}
            className="flex items-center gap-2 px-6 py-3 bg-[#FF007F] text-white font-black text-xs uppercase rounded-full hover:scale-105 transition-transform disabled:opacity-50"
          >
            <Zap size={14} />
            Publicar ahora
          </button>
        </div>
      </div>

      {/* Mejor horario */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <h3 className="font-black uppercase text-sm mb-4">Mejor horario para tu audiencia</h3>
        <div className="grid grid-cols-3 gap-4">
          {bestTimes.map(t => (
            <div key={t.day} className="bg-black/40 rounded-2xl p-4 text-center">
              <p className="text-xs font-bold">{t.day}</p>
              <p className="text-[10px] text-gray-500 mt-1">{t.time}</p>
              <p className={`text-[9px] font-black mt-1 ${t.color}`}>{t.level}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Programadas */}
      {scheduled.length > 0 && (
        <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
          <h3 className="font-black uppercase text-sm mb-4">Publicaciones programadas</h3>
          <div className="space-y-3">
            {scheduled.map(s => (
              <div key={s.id} className="flex items-center gap-4 bg-black/40 p-4 rounded-2xl">
                <Clock className="text-blue-400 shrink-0" size={18} />
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold truncate">{s.productName || 'Publicación'}</p>
                  <p className="text-[9px] text-gray-500">{s.platforms?.join(', ')} · {new Date(s.scheduledAt).toLocaleString('es-CO')}</p>
                </div>
                <span className="px-3 py-1 rounded-full text-[8px] font-black bg-blue-500/20 text-blue-400">Programado</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// TAB 4 – HISTORIAL
// ════════════════════════════════════════════════════════════════════════════
const HistoryTab = () => {
  const [posts, setPosts]   = useState([]);
  const [stats, setStats]   = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/social/history`,  { headers: authHeaders() }),
      axios.get(`${API}/social/stats`,    { headers: authHeaders() }),
    ]).then(([h, s]) => {
      setPosts(h.data);
      setStats(s.data);
    }).finally(() => setLoading(false));
  }, []);

  const statusConfig = {
    published:      { label: 'Publicado',    color: 'bg-green-500/20 text-green-400 border-green-500/20' },
    sent:           { label: 'Enviado',      color: 'bg-blue-500/20 text-blue-400 border-blue-500/20'  },
    pending_manual: { label: 'En tu celular', color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/20' },
  };

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <div className="w-12 h-12 border-4 border-[#D4AF37] border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Total publicaciones', value: stats.totalPosts || 0, color: 'text-[#D4AF37]' },
          { label: 'Publicadas',          value: stats.published || 0, color: 'text-green-400' },
          { label: 'Programadas',         value: stats.scheduled || 0, color: 'text-blue-400'  },
        ].map(s => (
          <div key={s.label} className="bg-white/5 rounded-3xl border border-white/10 p-6 text-center">
            <p className={`text-3xl font-black mb-1 ${s.color}`}>{s.value}</p>
            <p className="text-[9px] text-gray-500 uppercase">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Lista */}
      <div className="bg-white/5 rounded-[30px] border border-white/10 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-black uppercase text-sm">Publicaciones recientes</h3>
          <button onClick={() => window.location.reload()} className="text-gray-500 hover:text-white">
            <RefreshCw size={16} />
          </button>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-12 text-gray-600">
            <Instagram size={40} className="mx-auto mb-3" />
            <p className="text-sm">Aún no hay publicaciones. ¡Crea la primera!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {posts.map(p => {
              const sc = statusConfig[p.status] || { label: p.status, color: 'bg-gray-500/20 text-gray-400' };
              return (
                <div key={p.id} className="flex items-center gap-4 bg-black/40 p-4 rounded-2xl">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-[10px] font-black ${
                    p.platform === 'instagram' ? 'bg-gradient-to-tr from-yellow-500 via-pink-600 to-fuchsia-700 text-white'
                    : p.platform === 'tiktok' ? 'bg-white/10 text-white'
                    : 'bg-green-500/20 text-green-400'
                  }`}>
                    {p.platform === 'instagram' ? 'IG' : p.platform === 'tiktok' ? 'TT' : 'WA'}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold truncate">{p.productName || 'Publicación'}</p>
                    <p className="text-[9px] text-gray-500 truncate">{p.caption?.slice(0, 60)}...</p>
                    <p className="text-[9px] text-gray-600 mt-0.5">
                      {new Date(p.publishedAt || p.preparedAt).toLocaleString('es-CO')}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-[8px] font-black border ${sc.color}`}>{sc.label}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialMedia;
