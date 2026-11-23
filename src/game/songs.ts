// リズムゲームの収録曲リスト（作品データ）。作り方は docs/PRODUCTION.md の
// 「リズムゲーム（任意モジュール）」参照。
// frameInset: 3曲とも紙枠なし（目視で全辺フルブリードの絵と確認し、紙色バンド／
//   無彩色の明るいバンドの割合実測でも全辺 0.000 が 60px まで続く＝帯なしと判定。2026-11-23 実測）
import track01Audio from './assets/track01.mp3';
import track01Jacket from './assets/track01.jpg';
import track02Audio from './assets/track02.mp3';
import track02Jacket from './assets/track02.jpg';
import track03Audio from './assets/track03.mp3';
import track03Jacket from './assets/track03.jpg';

export interface GameSongDef {
  id: string;
  audioUrl: string;
  jacketUrl: string;
  frameInset: number;
  slidePosition?: string;
  accent: string;
  bonus?: boolean;
  album: string;
  genre: string;
}

const ALBUM_NAME = '青い火よ、消えないで ―サウンド単行本エンドロールソングス―';

export const SONG_DEFS: GameSongDef[] = [
  {
    id: 'aoibi',
    audioUrl: track01Audio,
    jacketUrl: track01Jacket,
    frameInset: 0,
    slidePosition: 'bottom',
    accent: '#51a8d6',
    album: ALBUM_NAME,
    genre: 'Dark Fantasy Rock',
  },
  {
    id: 'yonbyo',
    audioUrl: track02Audio,
    jacketUrl: track02Jacket,
    frameInset: 0,
    slidePosition: 'top',
    accent: '#51a7d6',
    album: ALBUM_NAME,
    genre: 'SF Ballad',
  },
  {
    id: 'anzen',
    audioUrl: track03Audio,
    jacketUrl: track03Jacket,
    frameInset: 0,
    accent: '#51d6c4',
    bonus: true,
    album: ALBUM_NAME,
    genre: 'Retro Synth-Pop',
  },
];
