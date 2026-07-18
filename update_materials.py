import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Update icons
content = content.replace(
    "import { BookOpen, Video, FileText, MessageCircle, Send, Award, Trash, Star, Play, CheckCircle, ChevronRight, Layout, Info, User, Volume2, Calendar } from 'lucide-react';",
    "import { BookOpen, Video, FileText, MessageCircle, Send, Award, Trash, Star, Play, CheckCircle, ChevronRight, Layout, Info, User, Volume2, Calendar, Paperclip, Download, Plus, X, Upload } from 'lucide-react';"
)

# Update Interface
interface_old = """export interface CourseMaterial {
  id?: string;
  subjectId: string;
  unit: number;
  type: 'video' | 'pdf' | 'article';
  title: string;
  contentUrl: string;
  description: string;
  createdAt: number;
}"""

interface_new = """export interface CourseMaterial {
  id?: string;
  subjectId: string;
  unit: number;
  type: 'video' | 'pdf' | 'article' | 'lesson';
  title: string;
  contentUrl: string;
  description: string;
  markdownNotes?: string;
  attachments?: { name: string; url: string }[];
  createdAt: number;
}"""

content = content.replace(interface_old, interface_new)

with open("src/features.tsx", "w") as f:
    f.write(content)
