import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {BestAnimesComponent} from './best-animes/best-animes.component';
import {BestMangasComponent} from './best-mangas/best-mangas.component';
import {UnderMaintenanceComponent} from './under-maintenance/under-maintenance.component'
const routes: Routes = [
  { path: 'best_animes', component: BestAnimesComponent },
  { path: 'best_mangas', component: BestMangasComponent },
  { path: 'under_maintenance', component: UnderMaintenanceComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
