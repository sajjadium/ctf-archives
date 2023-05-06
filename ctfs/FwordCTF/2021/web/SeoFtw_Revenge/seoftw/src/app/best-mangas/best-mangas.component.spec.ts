import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BestMangasComponent } from './best-mangas.component';

describe('BestMangasComponent', () => {
  let component: BestMangasComponent;
  let fixture: ComponentFixture<BestMangasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BestMangasComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BestMangasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
