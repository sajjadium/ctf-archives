import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnderMaintenanceComponent } from './under-maintenance.component';

describe('UnderMaintenanceComponent', () => {
  let component: UnderMaintenanceComponent;
  let fixture: ComponentFixture<UnderMaintenanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnderMaintenanceComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UnderMaintenanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
