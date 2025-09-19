import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Footer } from './componetes/layout/footer/footer';
import { Header } from './componetes/layout/header/header';
import { Principal } from './componetes/paginas/principal/principal';

@Component({
  selector: 'app-root',
  imports: [Principal, Footer, Header],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('Diparma');
}
